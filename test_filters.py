#!/usr/bin/env python3
"""
Script pour tester les filtres personnalisés
Usage: python3 test_filters.py
"""

import os
import django
from django.template import Template, Context
from django.db.models import Sum

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

from customers.models import Customer
from accounts.models import Account

def test_filters():
    """Test des filtres personnalisés"""
    
    print("🧪 Test des filtres personnalisés...")
    
    # Test 1: Vérifier que les filtres sont chargés
    try:
        from core.templatetags.bank_filters import sum_balance, sum_accounts
        print("✅ Filtres importés avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        return
    
    # Test 2: Test du filtre sum_balance
    try:
        customer = Customer.objects.first()
        if customer:
            accounts = customer.accounts.all()
            total_balance = sum_balance(accounts)
            print(f"✅ Filtre sum_balance fonctionne : {total_balance} FCFA")
        else:
            print("⚠️ Aucun client trouvé pour tester")
    except Exception as e:
        print(f"❌ Erreur avec sum_balance : {e}")
    
    # Test 3: Test du filtre sum_accounts
    try:
        from banks.models import Bank
        bank = Bank.objects.first()
        if bank:
            customers = bank.customers.all()
            total_accounts = sum_accounts(customers)
            print(f"✅ Filtre sum_accounts fonctionne : {total_accounts} comptes")
        else:
            print("⚠️ Aucune banque trouvée pour tester")
    except Exception as e:
        print(f"❌ Erreur avec sum_accounts : {e}")
    
    # Test 4: Test avec template Django
    try:
        template_string = """
        {% load bank_filters %}
        {% with total_balance=customer.accounts.all|sum_balance %}
            Solde total: {{ total_balance|floatformat:0 }} FCFA
        {% endwith %}
        """
        
        customer = Customer.objects.first()
        if customer:
            template = Template(template_string)
            context = Context({'customer': customer})
            result = template.render(context)
            print(f"✅ Template Django fonctionne : {result.strip()}")
        else:
            print("⚠️ Aucun client trouvé pour tester le template")
    except Exception as e:
        print(f"❌ Erreur avec le template : {e}")
    
    print("\n🎉 Test terminé !")

if __name__ == "__main__":
    test_filters()