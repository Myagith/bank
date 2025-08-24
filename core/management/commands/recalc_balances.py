from django.core.management.base import BaseCommand
from django.db.models import Sum, Q
from accounts.models import Account
from transactions.models import Transaction


class Command(BaseCommand):
    help = "Recalcule tous les soldes des comptes à partir des transactions"

    def handle(self, *args, **options):
        updated = 0
        for account in Account.objects.all():
            # Selon la demande: DEPOT diminue le solde du compte source
            incoming = Transaction.objects.filter(
                Q(type=Transaction.Type.TRANSFER, destination_account=account)
            ).aggregate(total=Sum('amount'))['total'] or 0

            outgoing = Transaction.objects.filter(
                Q(type=Transaction.Type.DEPOSIT, account=account) |
                Q(type=Transaction.Type.WITHDRAW, account=account) |
                Q(type=Transaction.Type.TRANSFER, account=account)
            ).aggregate(total=Sum('amount'))['total'] or 0

            new_balance = incoming - outgoing
            if account.balance != new_balance:
                account.balance = new_balance
                account.save(update_fields=['balance'])
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Recalcul terminé. {updated} comptes mis à jour."))