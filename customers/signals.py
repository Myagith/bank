from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
import random
from .models import Customer
from accounts.models import Account
from transactions.models import Transaction


@receiver(post_save, sender=Customer)
def seed_customer_demo(sender, instance: Customer, created: bool, **kwargs):
    if not created:
        return
    # Crée 1-2 comptes avec quelques transactions pour le dashboard
    num_accounts = random.randint(1, 2)
    for j in range(num_accounts):
        acc = Account.objects.create(
            customer=instance,
            number=f"ACC{instance.id:05d}{j:02d}",
            type='CHECKING',
            balance=Decimal('0.00')
        )
        # Génère 3-6 transactions
        for k in range(random.randint(3, 6)):
            amount = Decimal(random.randint(20, 300))
            ttype = random.choice(['DEPOSIT','WITHDRAW'])
            tx = Transaction.objects.create(
                account=acc,
                type=ttype,
                amount=amount,
                reference=f"AUTO-{instance.id}-{j}-{k}",
                description="Données démo"
            )
            # Balance sera ajusté par signal post_save Transaction