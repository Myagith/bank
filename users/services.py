import os
import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import User


def generate_otp() -> str:
    return f"{random.randint(0, 999999):06d}"


def send_otp_email(user: User) -> None:
    default_code = os.getenv('DEFAULT_OTP_CODE')
    user.otp_code = default_code if default_code and len(default_code) == 6 else generate_otp()
    user.otp_expires_at = timezone.now() + timedelta(minutes=10)
    user.save(update_fields=["otp_code", "otp_expires_at"])
    app_name = os.getenv('BANK_NAME', 'BANK')
    subject = os.getenv('OTP_EMAIL_SUBJECT', f"{app_name} - Code de connexion")
    template = os.getenv(
        'OTP_EMAIL_BODY',
        "Bonjour {username},\n\nVotre code de connexion est: {code}.\nIl expire dans {expires_minutes} minutes.\n\n{app_name}")
    message = template.format(
        username=user.username,
        code=user.otp_code,
        expires_minutes=10,
        app_name=app_name,
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)


def send_welcome_email(user: User, raw_password: str) -> None:
    app_name = os.getenv('BANK_NAME', 'BANK')
    subject = os.getenv('WELCOME_EMAIL_SUBJECT', f"Bienvenue sur {app_name}")
    template = os.getenv(
        'WELCOME_EMAIL_BODY',
        "Bonjour {username},\n\nVotre compte a été créé.\nIdentifiant: {username}\nMot de passe initial: {password}\n\nMerci d'utiliser {app_name}.")
    message = template.format(username=user.username, password=raw_password, app_name=app_name)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)


def get_user_accounts(user: User):
    """
    Retourne les comptes appartenant logiquement à l'utilisateur connecté.
    Priorité:
      0) s'il existe Customer.user = user, l'utiliser
      1) email exact entre User et Customer
      2) username correspond à Customer.name ou client_no
    """
    from customers.models import Customer
    from accounts.models import Account

    if not getattr(user, 'is_authenticated', False):
        return Account.objects.none()

    # 0) Lien direct FK si présent
    direct = Customer.objects.filter(user=user)
    if direct.exists():
        return Account.objects.filter(customer__in=direct)

    candidates = Customer.objects.none()

    if user.email:
        candidates = Customer.objects.filter(email__iexact=user.email)

    if not candidates.exists():
        candidates = Customer.objects.filter(
            Q(name__iexact=user.username) | Q(client_no__iexact=user.username)
        )

    if not candidates.exists():
        return Account.objects.none()

    return Account.objects.filter(customer__in=candidates)