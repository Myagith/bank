from django import forms
from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["customer", "number", "type", "status", "balance"]
        labels = {
            'customer': 'Client',
            'number': 'Numéro de compte',
            'type': 'Type de compte',
            'status': 'Statut',
            'balance': 'Solde initial'
        }
        help_texts = {
            'number': 'Numéro unique du compte (ex: FR123456789)',
            'balance': 'Solde initial du compte en euros'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les widgets
        self.fields['type'].widget = forms.Select(
            choices=Account.AccountType.choices,
            attrs={'class': 'form-select'}
        )
        self.fields['status'].widget = forms.Select(
            choices=Account.Status.choices,
            attrs={'class': 'form-select'}
        )
        self.fields['customer'].widget.attrs.update({'class': 'form-select'})
        self.fields['number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: FR123456789'
        })
        self.fields['balance'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0'
        })

    def clean_number(self):
        value = self.cleaned_data["number"].strip()
        if not value:
            raise forms.ValidationError("Le numéro de compte est obligatoire.")
        if Account.objects.exclude(pk=self.instance.pk).filter(number__iexact=value).exists():
            raise forms.ValidationError("Ce numéro de compte existe déjà.")
        return value.upper()

    def clean_balance(self):
        value = self.cleaned_data["balance"]
        if value < 0:
            raise forms.ValidationError("Le solde ne peut pas être négatif.")
        return value