from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction
from banks.models import Bank
from customers.models import Customer


class Command(BaseCommand):
    help = "Génère des données de démo pour un utilisateur (client) existant: comptes + transactions"

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username du User cible')
        parser.add_argument('--email', type=str, help='Email du User cible')
        parser.add_argument('--bank', type=str, default='Banque Atlantique', help='Nom de banque (créée si absente)')

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get('username')
        email = options.get('email')
        bank_name = options.get('bank')

        if not username and not email:
            raise CommandError('Fournir --username ou --email')

        user = None
        if username:
            user = User.objects.filter(username=username).first()
        if not user and email:
            user = User.objects.filter(email=email).first()
        if not user:
            raise CommandError('Utilisateur introuvable')

        bank, _ = Bank.objects.get_or_create(
            name=bank_name,
            defaults={'country': "Côte d'Ivoire", 'city': 'Abidjan', 'email': 'contact@demo.ci', 'phone': '+22501020304'}
        )

        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={
                'bank': bank,
                'name': user.username,
                'email': user.email or f"{user.username}@demo.ci",
                'client_no': f"AUT-{user.id:05d}",
                'phone': '+22501020304'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Customer créé pour {user.username}'))
        else:
            self.stdout.write(f'Customer déjà existant pour {user.username}')

        # Le signal Customer va créer comptes + transactions
        self.stdout.write(self.style.SUCCESS('Données démo en cours de génération (via signal)...'))
        self.stdout.write(self.style.SUCCESS('Terminé.'))