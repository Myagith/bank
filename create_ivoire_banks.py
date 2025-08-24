#!/usr/bin/env python3
"""
Script pour créer des données de démonstration avec des banques ivoiriennes
Usage: python3 create_ivoire_banks.py
"""

import os
import django
from decimal import Decimal
from django.utils import timezone

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

from banks.models import Bank
from customers.models import Customer
from accounts.models import Account

def create_ivoire_banks():
    """Créer des banques ivoiriennes de démonstration"""
    
    print("🏦 Création de banques ivoiriennes de démonstration...")
    
    # Banques ivoiriennes réelles
    banks_data = [
        {
            'name': 'Banque Atlantique',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@banqueatlantique.ci',
            'phone': '+225 27 22 49 49 49'
        },
        {
            'name': 'Société Générale de Banques en Côte d\'Ivoire (SGBCI)',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@sgci.ci',
            'phone': '+225 27 22 49 49 50'
        },
        {
            'name': 'Banque Internationale pour le Commerce et l\'Industrie de la Côte d\'Ivoire (BICICI)',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@bicici.ci',
            'phone': '+225 27 22 49 49 51'
        },
        {
            'name': 'Ecobank Côte d\'Ivoire',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@ecobank.ci',
            'phone': '+225 27 22 49 49 52'
        },
        {
            'name': 'Banque de l\'Habitat de Côte d\'Ivoire (BHCI)',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@bhci.ci',
            'phone': '+225 27 22 49 49 53'
        },
        {
            'name': 'Banque Régionale de Solidarité (BRS)',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@brs.ci',
            'phone': '+225 27 22 49 49 54'
        },
        {
            'name': 'Banque Nationale d\'Investissement (BNI)',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@bni.ci',
            'phone': '+225 27 22 49 49 55'
        },
        {
            'name': 'Banque de l\'Agriculture et du Développement Rural (BADR)',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@badr.ci',
            'phone': '+225 27 22 49 49 56'
        },
        {
            'name': 'Banque Populaire de Côte d\'Ivoire (BPCI)',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@bpci.ci',
            'phone': '+225 27 22 49 49 57'
        },
        {
            'name': 'Banque de l\'Union (BU)',
            'country': 'Côte d\'Ivoire',
            'city': 'Abidjan',
            'email': 'contact@bu.ci',
            'phone': '+225 27 22 49 49 58'
        }
    ]
    
    banks = []
    for bank_data in banks_data:
        bank, created = Bank.objects.get_or_create(
            name=bank_data['name'],
            defaults=bank_data
        )
        banks.append(bank)
        if created:
            print(f"✅ Banque créée : {bank.name}")
    
    # Créer des clients ivoiriens
    customers_data = [
        {'name': 'Kouassi Jean', 'email': 'kouassi.jean@email.ci', 'client_no': 'CLI001', 'phone': '+225 07 12 34 56 78'},
        {'name': 'Traoré Fatou', 'email': 'traore.fatou@email.ci', 'client_no': 'CLI002', 'phone': '+225 07 23 45 67 89'},
        {'name': 'Koné Moussa', 'email': 'kone.moussa@email.ci', 'client_no': 'CLI003', 'phone': '+225 07 34 56 78 90'},
        {'name': 'Ouattara Aminata', 'email': 'ouattara.aminata@email.ci', 'client_no': 'CLI004', 'phone': '+225 07 45 67 89 01'},
        {'name': 'Bamba Issouf', 'email': 'bamba.issouf@email.ci', 'client_no': 'CLI005', 'phone': '+225 07 56 78 90 12'},
        {'name': 'Diabaté Mariam', 'email': 'diabate.mariam@email.ci', 'client_no': 'CLI006', 'phone': '+225 07 67 89 01 23'},
        {'name': 'Yao Koffi', 'email': 'yao.koffi@email.ci', 'client_no': 'CLI007', 'phone': '+225 07 78 90 12 34'},
        {'name': 'Coulibaly Aïcha', 'email': 'coulibaly.aicha@email.ci', 'client_no': 'CLI008', 'phone': '+225 07 89 01 23 45'},
        {'name': 'Soro Adama', 'email': 'soro.adama@email.ci', 'client_no': 'CLI009', 'phone': '+225 07 90 12 34 56'},
        {'name': 'Kouamé Grace', 'email': 'kouame.grace@email.ci', 'client_no': 'CLI010', 'phone': '+225 07 01 23 45 67'},
        {'name': 'Bénié Kouassi', 'email': 'benie.kouassi@email.ci', 'client_no': 'CLI011', 'phone': '+225 07 12 34 56 78'},
        {'name': 'N\'Guessan Affoué', 'email': 'nguessan.affoue@email.ci', 'client_no': 'CLI012', 'phone': '+225 07 23 45 67 89'},
        {'name': 'Tano Kouamé', 'email': 'tano.kouame@email.ci', 'client_no': 'CLI013', 'phone': '+225 07 34 56 78 90'},
        {'name': 'Aka N\'Guessan', 'email': 'aka.nguessan@email.ci', 'client_no': 'CLI014', 'phone': '+225 07 45 67 89 01'},
        {'name': 'Kouassi Yao', 'email': 'kouassi.yao@email.ci', 'client_no': 'CLI015', 'phone': '+225 07 56 78 90 12'},
    ]
    
    customers = []
    for i, customer_data in enumerate(customers_data):
        customer, created = Customer.objects.get_or_create(
            client_no=customer_data['client_no'],
            defaults={
                **customer_data,
                'bank': banks[i % len(banks)]  # Répartir les clients entre les banques
            }
        )
        customers.append(customer)
        if created:
            print(f"✅ Client créé : {customer.name} ({customer.client_no})")
    
    # Créer des comptes avec des montants en FCFA
    account_types = ['CHECKING', 'SAVINGS']
    account_numbers = [
        'CI1234567890123456789012',  # 24 caractères
        'CI2345678901234567890123',
        'CI3456789012345678901234',
        'CI4567890123456789012345',
        'CI5678901234567890123456',
        'CI6789012345678901234567',
        'CI7890123456789012345678',
        'CI8901234567890123456789',
        'CI9012345678901234567890',
        'CI0123456789012345678901',
        'CI1111111111111111111111',
        'CI2222222222222222222222',
        'CI3333333333333333333333',
        'CI4444444444444444444444',
        'CI5555555555555555555555',
        'CI6666666666666666666666',
        'CI7777777777777777777777',
        'CI8888888888888888888888',
        'CI9999999999999999999999',
        'CI0000000000000000000000',
    ]
    
    # Montants en FCFA (1 EUR ≈ 650 FCFA)
    balances_fcfa = [
        Decimal('125000'), Decimal('342000'), Decimal('89000'), Decimal('567000'),
        Decimal('123000'), Decimal('789000'), Decimal('456000'), Decimal('234000'),
        Decimal('678000'), Decimal('345000'), Decimal('901000'), Decimal('567000'),
        Decimal('123000'), Decimal('789000'), Decimal('456000'), Decimal('234000'),
        Decimal('678000'), Decimal('345000'), Decimal('901000'), Decimal('567000'),
    ]
    
    # Créer des comptes avec différentes distributions
    accounts_created = 0
    
    # Client 1 : 1 compte
    account, created = Account.objects.get_or_create(
        number=account_numbers[0],
        defaults={
            'customer': customers[0],
            'type': 'CHECKING',
            'status': 'OPEN',
            'balance': balances_fcfa[0]
        }
    )
    if created:
        print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
        accounts_created += 1
    
    # Client 2 : 3 comptes
    for i in range(1, 4):
        account, created = Account.objects.get_or_create(
            number=account_numbers[i],
            defaults={
                'customer': customers[1],
                'type': account_types[i % 2],
                'status': 'OPEN',
                'balance': balances_fcfa[i]
            }
        )
        if created:
            print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
            accounts_created += 1
    
    # Client 3 : 7 comptes
    for i in range(4, 11):
        account, created = Account.objects.get_or_create(
            number=account_numbers[i],
            defaults={
                'customer': customers[2],
                'type': account_types[i % 2],
                'status': 'OPEN' if i < 10 else 'CLOSED',
                'balance': balances_fcfa[i % len(balances_fcfa)]
            }
        )
        if created:
            print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
            accounts_created += 1
    
    # Client 4 : 12 comptes
    for i in range(11, 20):
        account, created = Account.objects.get_or_create(
            number=account_numbers[i],
            defaults={
                'customer': customers[3],
                'type': account_types[i % 2],
                'status': 'OPEN' if i < 18 else 'CLOSED',
                'balance': balances_fcfa[i % len(balances_fcfa)]
            }
        )
        if created:
            print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
            accounts_created += 1
    
    # Ajouter quelques comptes pour les autres clients
    for i in range(4, len(customers)):
        account, created = Account.objects.get_or_create(
            number=f"CI{i:06d}000000000000000000"[:24],
            defaults={
                'customer': customers[i],
                'type': account_types[i % 2],
                'status': 'OPEN',
                'balance': balances_fcfa[i % len(balances_fcfa)]
            }
        )
        if created:
            print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
            accounts_created += 1
    
    print(f"\n🎉 Création terminée !")
    print(f"📊 Statistiques :")
    print(f"   • Banques : {Bank.objects.count()}")
    print(f"   • Clients : {Customer.objects.count()}")
    print(f"   • Comptes : {Account.objects.count()}")
    print(f"   • Comptes ouverts : {Account.objects.filter(status='OPEN').count()}")
    print(f"   • Comptes fermés : {Account.objects.filter(status='CLOSED').count()}")
    print(f"   • Comptes courants : {Account.objects.filter(type='CHECKING').count()}")
    print(f"   • Comptes épargne : {Account.objects.filter(type='SAVINGS').count()}")
    
    # Afficher la distribution des clients
    print(f"\n👥 Distribution des clients par nombre de comptes :")
    from django.db.models import Count
    customer_account_counts = Customer.objects.annotate(
        account_count=Count('accounts')
    ).values('name', 'account_count').order_by('account_count')
    
    for customer in customer_account_counts:
        print(f"   • {customer['name']} : {customer['account_count']} compte(s)")
    
    # Afficher les banques avec le nombre de clients
    print(f"\n🏦 Distribution des banques par nombre de clients :")
    bank_customer_counts = Bank.objects.annotate(
        customer_count=Count('customers')
    ).values('name', 'customer_count').order_by('-customer_count')
    
    for bank in bank_customer_counts:
        print(f"   • {bank['name']} : {bank['customer_count']} client(s)")

if __name__ == "__main__":
    create_ivoire_banks()