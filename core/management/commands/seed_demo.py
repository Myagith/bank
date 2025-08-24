from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import random

from banks.models import Bank
from customers.models import Customer
from accounts.models import Account
from transactions.models import Transaction


class Command(BaseCommand):
    help = "Seed la base avec 15 banques, un admin, des clients, comptes et transactions."

    def handle(self, *args, **options):
        User = get_user_model()

        # Admin
        admin, created = User.objects.get_or_create(
            username='admin', defaults={'email': 'admin@bank.local', 'role': 'ADMIN', 'can_login': True}
        )
        if created:
            admin.set_password('Admin123!')
            admin.save()

        # Banks
        banks = []
        bank_names = [
            'Banque Atlantique','Société Générale CI','NSIA Banque','Bank of Africa','Ecobank','UBA','Versus Bank',
            'Bridge Bank','Coris Bank','BICICI','BACIM','FinBank','Orange Bank','Wizall Bank','Afriland Bank'
        ]
        # Préparer la liste des champs Bank pour gérer les variantes de schéma
        bank_field_names = {f.name for f in Bank._meta.get_fields()}
        for name in bank_names:
            defaults = {
                'country': "Côte d'Ivoire",
                'city': 'Abidjan',
                'email': f"contact@{name.lower().replace(' ', '')}.ci",
                'phone': '+22501020304',
            }
            # Renseigner des valeurs par défaut si ces champs existent et sont NOT NULL
            for extra in ['owner', 'ceo', 'director', 'director_general', 'general_manager', 'proprietor', 'owner_name']:
                if extra in bank_field_names:
                    defaults[extra] = 'Direction Générale'

            bank, _ = Bank.objects.get_or_create(name=name, defaults=defaults)
            banks.append(bank)

        # Customers, Accounts and Transactions
        customer_field_names = {f.name for f in Customer._meta.get_fields()}
        all_accounts = []
        for i in range(1, 31):
            bank = random.choice(banks)
            cust_defaults = {
                'name': f'Client {i}',
                'email': f'client{i}@demo.ci',
                'phone': '+22501020304',
            }
            if 'address' in customer_field_names:
                cust_defaults['address'] = 'Abidjan, CI'
            customer, _ = Customer.objects.get_or_create(
                client_no=f'C{i:05d}', bank=bank,
                defaults=cust_defaults
            )
            # Accounts
            for j in range(random.randint(1, 2)):
                acc, _ = Account.objects.get_or_create(
                    customer=customer,
                    number=f'CI{bank.id}{i:05d}{j:02d}',
                    defaults={'type': 'CHECKING', 'balance': Decimal('0.00')}
                )
                # Transactions
                for k in range(random.randint(3, 8)):
                    amount = Decimal(random.randint(10, 500))
                    ttype = random.choice(['DEPOSIT','WITHDRAW','TRANSFER'])
                    tx = Transaction.objects.create(account=acc, type=ttype, amount=amount, reference=f'DEMO-{i}-{j}-{k}')
                    # Update balance roughly (matching services.post_transaction logic simplified here)
                    if ttype == 'DEPOSIT' or ttype == 'TRANSFER':
                        acc.balance += amount
                    elif ttype == 'WITHDRAW' and acc.balance > amount:
                        acc.balance -= amount
                acc.save()
                all_accounts.append(acc)

        # Booster les soldes: mettre des montants élevés positifs
        for acc in all_accounts:
            # entre 500 000 et 2 000 000 (2 décimales)
            base = random.randint(500000, 2000000)
            acc.balance = Decimal(base)
            acc.save(update_fields=['balance'])

        # Forcer 3 comptes négatifs s'il y a assez de comptes
        if len(all_accounts) >= 3:
            negative_samples = random.sample(all_accounts, 3)
            for acc in negative_samples:
                acc.balance = Decimal(-random.randint(1000, 50000))
                acc.save(update_fields=['balance'])

        # Ajouter un client VIP avec un gros montant
        vip_bank = random.choice(banks)
        vip_customer, _ = Customer.objects.get_or_create(
            client_no='VIP00001', bank=vip_bank,
            defaults={'name': 'VIP Client', 'email': 'vip@demo.ci', 'phone': '+2250700000000'}
        )
        # Créer (ou lier) un utilisateur VIP pour connexion
        vip_user, created_user = User.objects.get_or_create(
            username='vip',
            defaults={'email': 'vip@demo.ci', 'role': 'CLIENT', 'can_login': True}
        )
        if created_user:
            vip_user.set_password('Vip12345!')
            vip_user.save()
        if not vip_customer.user:
            vip_customer.user = vip_user
            vip_customer.save(update_fields=['user'])

        vip_account, _ = Account.objects.get_or_create(
            customer=vip_customer,
            number=f'CI{vip_bank.id}VIP00001',
            defaults={'type': 'CHECKING', 'balance': Decimal('0.00')}
        )
        vip_account.balance = Decimal('5000000.00')  # 5 000 000 pour tests de transferts
        vip_account.save(update_fields=['balance'])

        self.stdout.write(self.style.SUCCESS('Seed terminé. Utilisateur admin/Admin123! — VIP: vip/Vip12345!'))

