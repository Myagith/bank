from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from customers.models import Customer


class Command(BaseCommand):
    help = "Associe automatiquement les Customers aux Users via email/username/client_no"

    def handle(self, *args, **options):
        User = get_user_model()
        linked = 0
        for customer in Customer.objects.filter(user__isnull=True):
            user = None
            # 1) email
            if customer.email:
                user = User.objects.filter(email__iexact=customer.email).first()
            # 2) username == name or client_no
            if not user:
                user = User.objects.filter(
                    Q(username__iexact=customer.name) | Q(username__iexact=customer.client_no)
                ).first()
            if user:
                customer.user = user
                customer.save(update_fields=["user"])
                linked += 1
                self.stdout.write(self.style.SUCCESS(f"Lié: Customer {customer.id} -> User {user.username}"))
        self.stdout.write(self.style.SUCCESS(f"Terminé. {linked} liaisons créées."))