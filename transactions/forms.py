from django import forms
from .models import Transaction
from accounts.models import Account


class TransactionForm(forms.ModelForm):
    destination_account = forms.ModelChoiceField(
        queryset=Account.objects.filter(status='OPEN'),
        required=False,
        empty_label="Sélectionnez un compte destinataire",
        label="Compte destinataire",
        help_text="Obligatoire pour les transferts"
    )
    
    class Meta:
        model = Transaction
        fields = ["account", "type", "amount", "reference", "description", "destination_account"]
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Description optionnelle'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Le montant doit être positif.")
        return amount
    
    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('type')
        destination_account = cleaned_data.get('destination_account')
        account = cleaned_data.get('account')
        
        # Validation pour les transferts
        if transaction_type == Transaction.Type.TRANSFER:
            if not destination_account:
                raise forms.ValidationError("Un compte destinataire est obligatoire pour les transferts.")
            
            if destination_account == account:
                raise forms.ValidationError("Vous ne pouvez pas transférer vers le même compte.")
        
        return cleaned_data