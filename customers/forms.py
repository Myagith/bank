from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["bank", "name", "email", "client_no", "phone"]
        labels = {
            'bank': 'Banque',
            'name': 'Nom complet',
            'email': 'Adresse email',
            'client_no': 'Numéro de client',
            'phone': 'Numéro de téléphone'
        }
        help_texts = {
            'name': 'Nom et prénom du client',
            'email': 'Adresse email valide',
            'client_no': 'Numéro unique du client (ex: CLI001)',
            'phone': 'Numéro de téléphone avec indicatif'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les widgets
        self.fields['bank'].widget.attrs.update({'class': 'form-select'})
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: Jean Dupont'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: jean.dupont@email.com'
        })
        self.fields['client_no'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: CLI001'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: 06 12 34 56 78'
        })

    def clean_client_no(self):
        value = self.cleaned_data["client_no"].strip()
        if not value:
            raise forms.ValidationError("Le numéro de client est obligatoire.")
        if Customer.objects.exclude(pk=self.instance.pk).filter(client_no__iexact=value).exists():
            raise forms.ValidationError("Ce numéro de client existe déjà.")
        return value.upper()

    def clean_email(self):
        value = self.cleaned_data["email"].strip()
        if not value:
            raise forms.ValidationError("L'adresse email est obligatoire.")
        if Customer.objects.exclude(pk=self.instance.pk).filter(email__iexact=value).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return value.lower()

    def clean_name(self):
        value = self.cleaned_data["name"].strip()
        if not value:
            raise forms.ValidationError("Le nom du client est obligatoire.")
        return value.title()