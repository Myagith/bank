from django.contrib import admin
from django.conf import settings
from .models import User
from .services import send_welcome_email


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active", "is_superuser")
    search_fields = ("username", "email")

    def save_model(self, request, obj: User, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        # Envoi optionnel d'email de bienvenue après création via Admin
        if is_new and obj.email and getattr(settings, 'EMAIL_SEND_WELCOME_ON_ADMIN_CREATE', False):
            try:
                send_welcome_email(obj)
            except Exception:
                # Laisser l'exception remonter seulement si EMAIL_FAIL_SILENTLY est False
                if not getattr(settings, 'EMAIL_FAIL_SILENTLY', True):
                    raise

# Register your models here.
