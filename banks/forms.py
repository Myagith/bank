from django import forms
from .models import Bank


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ["name", "country", "city", "email", "phone"]
        labels = {
            'name': 'Nom de la banque',
            'country': 'Pays',
            'city': 'Ville',
            'email': 'Adresse email',
            'phone': 'Numéro de téléphone'
        }
        help_texts = {
            'name': 'Nom officiel de la banque',
            'country': 'Pays où se trouve la banque',
            'city': 'Ville principale de la banque',
            'email': 'Adresse email de contact',
            'phone': 'Numéro de téléphone avec indicatif'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser les widgets
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: Banque Atlantique'
        })
        self.fields['country'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['city'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: Abidjan'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: contact@banqueatlantique.ci'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ex: +225 27 22 49 49 49'
        })
        
        # Définir Côte d'Ivoire comme pays par défaut
        if not self.instance.pk:  # Nouvelle banque
            self.fields['country'].initial = 'Côte d\'Ivoire'

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Le nom de la banque est obligatoire.")
        if Bank.objects.exclude(pk=self.instance.pk).filter(name__iexact=name).exists():
            raise forms.ValidationError("Une banque avec ce nom existe déjà.")
        return name.title()

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if not email:
            raise forms.ValidationError("L'adresse email est obligatoire.")
        if Bank.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email.lower()

    def clean_country(self):
        country = self.cleaned_data["country"].strip()
        if not country:
            raise forms.ValidationError("Le pays est obligatoire.")
        return country

    def clean_city(self):
        city = self.cleaned_data["city"].strip()
        if not city:
            raise forms.ValidationError("La ville est obligatoire.")
        return city.title()