from decimal import Decimal
from django.db import transaction as db_transaction
from django.core.mail import send_mail
from django.conf import settings
import os
from .models import Transaction
from accounts.models import Account


def send_transaction_email(transaction: Transaction, recipient_email: str, email_type: str) -> None:
    """Envoie un email de notification de transaction"""
    try:
        app_name = os.getenv('BANK_NAME', 'PAYGUARD')
        
        if email_type == 'deposit_confirmation':
            subject = f"{app_name} - Confirmation de dépôt"
            message = f"""
Bonjour,

✅ Votre dépôt a été effectué avec succès !

📊 Détails de l'opération :
• Type : Dépôt
• Montant : {transaction.amount} €
• Compte : {transaction.account.number}
• Référence : {transaction.reference}
• Date : {transaction.created_at.strftime('%d/%m/%Y à %H:%M')}

💰 Nouveau solde : {transaction.account.balance} €

Merci de votre confiance !

Cordialement,
L'équipe {app_name}
            """
        
        elif email_type == 'withdraw_confirmation':
            subject = f"{app_name} - Confirmation de retrait"
            message = f"""
Bonjour,

✅ Votre retrait a été effectué avec succès !

📊 Détails de l'opération :
• Type : Retrait
• Montant : {transaction.amount} €
• Compte : {transaction.account.number}
• Référence : {transaction.reference}
• Date : {transaction.created_at.strftime('%d/%m/%Y à %H:%M')}

💰 Nouveau solde : {transaction.account.balance} €

Merci de votre confiance !

Cordialement,
L'équipe {app_name}
            """
        
        elif email_type == 'transfer_sent':
            subject = f"{app_name} - Transfert envoyé"
            message = f"""
Bonjour,

✅ Votre transfert a été envoyé avec succès !

📊 Détails de l'opération :
• Type : Transfert sortant
• Montant : {transaction.amount} €
• Compte émetteur : {transaction.account.number}
• Référence : {transaction.reference}
• Date : {transaction.created_at.strftime('%d/%m/%Y à %H:%M')}

💰 Nouveau solde : {transaction.account.balance} €

Merci de votre confiance !

Cordialement,
L'équipe {app_name}
            """
        
        elif email_type == 'transfer_received':
            subject = f"{app_name} - Transfert reçu"
            message = f"""
Bonjour,

🎉 Vous avez reçu un transfert !

📊 Détails de l'opération :
• Type : Transfert entrant
• Montant : {transaction.amount} €
• Compte destinataire : {transaction.account.number}
• Référence : {transaction.reference}
• Date : {transaction.created_at.strftime('%d/%m/%Y à %H:%M')}

💰 Nouveau solde : {transaction.account.balance} €

Merci de votre confiance !

Cordialement,
L'équipe {app_name}
            """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=settings.EMAIL_FAIL_SILENTLY
        )
        
    except Exception as e:
        print(f"Erreur envoi email transaction: {e}")


@db_transaction.atomic
def post_transaction(tx: Transaction) -> None:
    account: Account = tx.account
    
    # Traitement de la transaction
    if tx.type == Transaction.Type.DEPOSIT:
        # DEMANDE: un dépôt DIMINUE le solde
        account.balance = (account.balance or Decimal('0')) - tx.amount
        # Email de confirmation de dépôt
        if account.customer.email:
            send_transaction_email(tx, account.customer.email, 'deposit_confirmation')
            
    elif tx.type == Transaction.Type.WITHDRAW:
        if (account.balance or Decimal('0')) < tx.amount:
            raise ValueError('Insufficient funds')
        account.balance -= tx.amount
        # Email de confirmation de retrait
        if account.customer.email:
            send_transaction_email(tx, account.customer.email, 'withdraw_confirmation')
            
    elif tx.type == Transaction.Type.TRANSFER:
        # Pour les transferts, on crée deux transactions
        # 1. Débit sur le compte émetteur
        if (account.balance or Decimal('0')) < tx.amount:
            raise ValueError('Insufficient funds')
        account.balance -= tx.amount
        account.save(update_fields=['balance'])
        
        # Email à l'émetteur
        if account.customer.email:
            send_transaction_email(tx, account.customer.email, 'transfer_sent')
        
        # 2. Crédit sur le compte destinataire
        if tx.destination_account:
            dest_account = tx.destination_account
            dest_account.balance = (dest_account.balance or Decimal('0')) + tx.amount
            dest_account.save(update_fields=['balance'])
            
            # Créer une transaction de réception pour le destinataire
            receiving_tx = Transaction.objects.create(
                account=dest_account,
                type=Transaction.Type.DEPOSIT,  # Pour le destinataire, c'est un dépôt
                amount=tx.amount,
                reference=f"Reçu de {account.number}",
                description=f"Transfert reçu de {account.customer.name} ({account.number})"
            )
            
            # Email au destinataire
            if dest_account.customer.email:
                send_transaction_email(receiving_tx, dest_account.customer.email, 'transfer_received')
    
    account.save(update_fields=['balance'])