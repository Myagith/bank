from django.contrib import admin
from django.conf import settings
from .models import Customer
from users.services import send_welcome_email


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("client_no", "name", "email", "bank")
    search_fields = ("client_no", "name", "email")
    list_filter = ("bank",)

    def save_model(self, request, obj: Customer, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        # Envoi optionnel d'email de bienvenue après création via Admin
        if is_new and obj.email and getattr(settings, 'EMAIL_SEND_WELCOME_ON_ADMIN_CREATE_CUSTOMER', False):
            try:
                # On n'a pas de mot de passe ici; message sans mot de passe
                class DummyUser:
                    username = obj.name
                    email = obj.email
                    phone = obj.phone
                send_welcome_email(DummyUser())
            except Exception:
                if not getattr(settings, 'EMAIL_FAIL_SILENTLY', True):
                    raise
