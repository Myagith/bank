#!/usr/bin/env python3
"""
Script pour créer des données de démo pour les graphiques
Usage: python3 create_demo_data.py
"""

import os
import django
from django.utils import timezone
from datetime import timedelta
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

from users.models import User
from banks.models import Bank
from customers.models import Customer
from accounts.models import Account
from transactions.models import Transaction
from django.contrib.auth.hashers import make_password

def create_demo_data():
    """Crée des données de démo pour les graphiques"""
    
    print("🚀 Création des données de démo PAYGUARD")
    print("=" * 50)
    
    # 1. Créer des banques
    banks_data = [
        {'name': 'Banque Atlantique', 'country': 'Côte d\'Ivoire', 'city': 'Abidjan'},
        {'name': 'SG CI', 'country': 'Côte d\'Ivoire', 'city': 'Abidjan'},
        {'name': 'NSIA', 'country': 'Côte d\'Ivoire', 'city': 'Abidjan'},
        {'name': 'BOA', 'country': 'Côte d\'Ivoire', 'city': 'Abidjan'},
        {'name': 'UBA', 'country': 'Côte d\'Ivoire', 'city': 'Abidjan'},
        {'name': 'Ecobank', 'country': 'Côte d\'Ivoire', 'city': 'Abidjan'},
        {'name': 'SIB', 'country': 'Côte d\'Ivoire', 'city': 'Abidjan'},
    ]
    
    banks = []
    for bank_data in banks_data:
        bank, created = Bank.objects.get_or_create(
            name=bank_data['name'],
            defaults={
                'country': bank_data['country'],
                'city': bank_data['city'],
                'created_at': timezone.now() - timedelta(days=random.randint(30, 365))
            }
        )
        banks.append(bank)
        if created:
            print(f"✅ Banque créée: {bank.name}")
    
    # 2. Créer des utilisateurs clients
    clients_data = [
        {'username': 'client1', 'email': 'client1@example.com', 'first_name': 'Jean', 'last_name': 'Dupont'},
        {'username': 'client2', 'email': 'client2@example.com', 'first_name': 'Marie', 'last_name': 'Martin'},
        {'username': 'client3', 'email': 'client3@example.com', 'first_name': 'Pierre', 'last_name': 'Durand'},
        {'username': 'client4', 'email': 'client4@example.com', 'first_name': 'Sophie', 'last_name': 'Leroy'},
        {'username': 'client5', 'email': 'client5@example.com', 'first_name': 'Paul', 'last_name': 'Moreau'},
    ]
    
    customers = []
    for client_data in clients_data:
        # Créer l'utilisateur
        user, created = User.objects.get_or_create(
            username=client_data['username'],
            defaults={
                'email': client_data['email'],
                'first_name': client_data['first_name'],
                'last_name': client_data['last_name'],
                'password': make_password('Client123!'),
                'role': User.Role.CLIENT,
                'can_login': True,
                'date_joined': timezone.now() - timedelta(days=random.randint(10, 200))
            }
        )
        
        if created:
            print(f"✅ Utilisateur créé: {user.username}")
        
        # Créer le client
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={
                'name': f"{client_data['first_name']} {client_data['last_name']}",
                'bank': random.choice(banks),
                'phone': f"+225{random.randint(10000000, 99999999)}",
                'created_at': user.date_joined
            }
        )
        
        if created:
            print(f"✅ Client créé: {customer.name}")
        
        customers.append(customer)
    
    # 3. Créer des comptes
    accounts = []
    for customer in customers:
        # 1-2 comptes par client
        num_accounts = random.randint(1, 2)
        for i in range(num_accounts):
            account, created = Account.objects.get_or_create(
                customer=customer,
                number=f"FR{random.randint(100000000, 999999999)}",
                defaults={
                    'type': random.choice(['CHECKING', 'SAVINGS', 'BUSINESS']),
                    'balance': random.randint(1000, 50000),
                    'status': 'OPEN',
                    'created_at': customer.created_at + timedelta(days=random.randint(1, 30))
                }
            )
            
            if created:
                print(f"✅ Compte créé: {account.number} (Solde: {account.balance}€)")
            
            accounts.append(account)
    
    # 4. Créer des transactions
    transaction_types = ['DEPOSIT', 'WITHDRAW', 'TRANSFER']
    
    for account in accounts:
        # 5-15 transactions par compte
        num_transactions = random.randint(5, 15)
        
        for i in range(num_transactions):
            # Date aléatoire dans les 3 derniers mois
            transaction_date = timezone.now() - timedelta(
                days=random.randint(1, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            transaction_type = random.choice(transaction_types)
            amount = random.randint(100, 5000)
            
            transaction = Transaction.objects.create(
                account=account,
                type=transaction_type,
                amount=amount,
                reference=f"{transaction_type[:3]}{random.randint(1000, 9999)}",
                description=f"Transaction {transaction_type.lower()} de {amount}€",
                created_at=transaction_date
            )
            
            print(f"✅ Transaction créée: {transaction.type} {transaction.amount}€ sur {account.number}")
    
    print("\n🎉 Données de démo créées avec succès !")
    print(f"📊 Statistiques:")
    print(f"   • {len(banks)} banques")
    print(f"   • {len(customers)} clients")
    print(f"   • {len(accounts)} comptes")
    print(f"   • {Transaction.objects.count()} transactions")
    
    print("\n🔑 Identifiants de test:")
    for customer in customers:
        print(f"   • {customer.user.username} / Client123!")

if __name__ == "__main__":
    create_demo_data()