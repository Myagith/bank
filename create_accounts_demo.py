#!/usr/bin/env python3
"""
Script pour créer des données de démonstration pour les comptes
Usage: python3 create_accounts_demo.py
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
from users.models import User

def create_demo_accounts():
    """Créer des comptes de démonstration"""
    
    print("🏦 Création de données de démonstration pour les comptes...")
    
    # Créer des banques si elles n'existent pas
    banks_data = [
        {'name': 'Banque de France', 'country': 'France', 'city': 'Paris', 'email': 'contact@banquedefrance.fr', 'phone': '01 42 92 42 92'},
        {'name': 'Crédit Agricole', 'country': 'France', 'city': 'Paris', 'email': 'contact@credit-agricole.fr', 'phone': '01 43 23 45 67'},
        {'name': 'BNP Paribas', 'country': 'France', 'city': 'Paris', 'email': 'contact@bnpparibas.fr', 'phone': '01 40 14 45 46'},
        {'name': 'Société Générale', 'country': 'France', 'city': 'Paris', 'email': 'contact@socgen.fr', 'phone': '01 42 14 20 00'},
        {'name': 'LCL', 'country': 'France', 'city': 'Lyon', 'email': 'contact@lcl.fr', 'phone': '04 72 40 40 40'},
        {'name': 'Caisse d\'Épargne', 'country': 'France', 'city': 'Paris', 'email': 'contact@caisse-epargne.fr', 'phone': '01 58 40 40 40'},
        {'name': 'Banque Populaire', 'country': 'France', 'city': 'Paris', 'email': 'contact@banquepopulaire.fr', 'phone': '01 58 40 40 40'},
        {'name': 'Crédit Mutuel', 'country': 'France', 'city': 'Strasbourg', 'email': 'contact@creditmutuel.fr', 'phone': '03 88 14 14 14'},
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
    
    # Créer des clients si ils n'existent pas
    customers_data = [
        {'name': 'Jean Dupont', 'email': 'jean.dupont@email.com', 'client_no': 'CLI001', 'phone': '06 12 34 56 78'},
        {'name': 'Marie Martin', 'email': 'marie.martin@email.com', 'client_no': 'CLI002', 'phone': '06 23 45 67 89'},
        {'name': 'Pierre Durand', 'email': 'pierre.durand@email.com', 'client_no': 'CLI003', 'phone': '06 34 56 78 90'},
        {'name': 'Sophie Bernard', 'email': 'sophie.bernard@email.com', 'client_no': 'CLI004', 'phone': '06 45 67 89 01'},
        {'name': 'Michel Petit', 'email': 'michel.petit@email.com', 'client_no': 'CLI005', 'phone': '06 56 78 90 12'},
        {'name': 'Isabelle Moreau', 'email': 'isabelle.moreau@email.com', 'client_no': 'CLI006', 'phone': '06 67 89 01 23'},
        {'name': 'François Leroy', 'email': 'francois.leroy@email.com', 'client_no': 'CLI007', 'phone': '06 78 90 12 34'},
        {'name': 'Nathalie Roux', 'email': 'nathalie.roux@email.com', 'client_no': 'CLI008', 'phone': '06 89 01 23 45'},
        {'name': 'Philippe Simon', 'email': 'philippe.simon@email.com', 'client_no': 'CLI009', 'phone': '06 90 12 34 56'},
        {'name': 'Catherine Michel', 'email': 'catherine.michel@email.com', 'client_no': 'CLI010', 'phone': '06 01 23 45 67'},
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
    
    # Créer des comptes de démonstration
    account_types = ['CHECKING', 'SAVINGS']
    account_numbers = [
        'FR123456789012345678901234',
        'FR234567890123456789012345',
        'FR345678901234567890123456',
        'FR456789012345678901234567',
        'FR567890123456789012345678',
        'FR678901234567890123456789',
        'FR789012345678901234567890',
        'FR890123456789012345678901',
        'FR901234567890123456789012',
        'FR012345678901234567890123',
        'FR111111111111111111111111',
        'FR222222222222222222222222',
        'FR333333333333333333333333',
        'FR444444444444444444444444',
        'FR555555555555555555555555',
        'FR666666666666666666666666',
        'FR777777777777777777777777',
        'FR888888888888888888888888',
        'FR999999999999999999999999',
        'FR000000000000000000000000',
    ]
    
    balances = [
        Decimal('1250.50'), Decimal('3420.75'), Decimal('890.25'), Decimal('5670.00'),
        Decimal('1234.56'), Decimal('7890.12'), Decimal('4567.89'), Decimal('2345.67'),
        Decimal('6789.01'), Decimal('3456.78'), Decimal('9012.34'), Decimal('5678.90'),
        Decimal('1234.56'), Decimal('7890.12'), Decimal('4567.89'), Decimal('2345.67'),
        Decimal('6789.01'), Decimal('3456.78'), Decimal('9012.34'), Decimal('5678.90'),
    ]
    
    # Créer des comptes avec différentes distributions
    accounts_created = 0
    
    # Client 1 : 1 compte (pour tester le filtre "1 client")
    account, created = Account.objects.get_or_create(
        number=account_numbers[0],
        defaults={
            'customer': customers[0],
            'type': 'CHECKING',
            'status': 'OPEN',
            'balance': balances[0]
        }
    )
    if created:
        print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
        accounts_created += 1
    
    # Client 2 : 3 comptes (pour tester le filtre "2-5 clients")
    for i in range(1, 4):
        account, created = Account.objects.get_or_create(
            number=account_numbers[i],
            defaults={
                'customer': customers[1],
                'type': account_types[i % 2],
                'status': 'OPEN',
                'balance': balances[i]
            }
        )
        if created:
            print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
            accounts_created += 1
    
    # Client 3 : 7 comptes (pour tester le filtre "6-10 clients")
    for i in range(4, 11):
        account, created = Account.objects.get_or_create(
            number=account_numbers[i],
            defaults={
                'customer': customers[2],
                'type': account_types[i % 2],
                'status': 'OPEN' if i < 10 else 'CLOSED',
                'balance': balances[i % len(balances)]
            }
        )
        if created:
            print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
            accounts_created += 1
    
    # Client 4 : 12 comptes (pour tester le filtre "10+ clients")
    for i in range(11, 20):
        account, created = Account.objects.get_or_create(
            number=account_numbers[i],
            defaults={
                'customer': customers[3],
                'type': account_types[i % 2],
                'status': 'OPEN' if i < 18 else 'CLOSED',
                'balance': balances[i % len(balances)]
            }
        )
        if created:
            print(f"✅ Compte créé : {account.number} pour {account.customer.name}")
            accounts_created += 1
    
    # Ajouter quelques comptes pour les autres clients
    for i in range(4, len(customers)):
        account, created = Account.objects.get_or_create(
            number=f"FR{i:06d}000000000000000000",
            defaults={
                'customer': customers[i],
                'type': account_types[i % 2],
                'status': 'OPEN',
                'balance': balances[i % len(balances)]
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

if __name__ == "__main__":
    create_demo_accounts()