from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from .services import post_transaction


@receiver(post_save, sender=Transaction)
def handle_transaction_post_save(sender, instance: Transaction, created: bool, **kwargs):
    # Ne pas retraiter si déjà marqué processed (ou lors d'updates non pertinentes)
    if not created or instance.processed:
        return
    try:
        post_transaction(instance)
        instance.processed = True
        instance.save(update_fields=["processed"])
    except Exception:
        # Laisser l'erreur silencieuse côté signal; la vue/form gère déjà les erreurs
        pass