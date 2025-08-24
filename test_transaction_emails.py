#!/usr/bin/env python3
"""
Script de test pour vérifier l'envoi d'emails de transactions
Usage: python3 test_transaction_emails.py
"""

import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

def test_transaction_emails():
    """Test l'envoi d'emails de transactions"""
    try:
        app_name = os.getenv('BANK_NAME', 'PAYGUARD')
        
        # Test email de dépôt
        deposit_subject = f"{app_name} - Confirmation de dépôt"
        deposit_message = f"""
Bonjour,

✅ Votre dépôt a été effectué avec succès !

📊 Détails de l'opération :
• Type : Dépôt
• Montant : 1000.00 €
• Compte : FR123456789
• Référence : DEP001
• Date : 24/08/2024 à 14:30

💰 Nouveau solde : 1500.00 €

Merci de votre confiance !

Cordialement,
L'équipe {app_name}
        """
        
        # Test email de transfert envoyé
        transfer_sent_subject = f"{app_name} - Transfert envoyé"
        transfer_sent_message = f"""
Bonjour,

✅ Votre transfert a été envoyé avec succès !

📊 Détails de l'opération :
• Type : Transfert sortant
• Montant : 500.00 €
• Compte émetteur : FR123456789
• Référence : TRANS001
• Date : 24/08/2024 à 14:35

💰 Nouveau solde : 1000.00 €

Merci de votre confiance !

Cordialement,
L'équipe {app_name}
        """
        
        # Test email de transfert reçu
        transfer_received_subject = f"{app_name} - Transfert reçu"
        transfer_received_message = f"""
Bonjour,

🎉 Vous avez reçu un transfert !

📊 Détails de l'opération :
• Type : Transfert entrant
• Montant : 500.00 €
• Compte destinataire : FR987654321
• Référence : Reçu de FR123456789
• Date : 24/08/2024 à 14:35

💰 Nouveau solde : 2500.00 €

Merci de votre confiance !

Cordialement,
L'équipe {app_name}
        """
        
        # Email de test
        test_email = input("Entrez votre email pour tester les notifications de transactions : ").strip()
        if not test_email:
            test_email = "test@example.com"
        
        print(f"🔄 Envoi des emails de test à : {test_email}")
        print(f"📧 Backend : {settings.EMAIL_BACKEND}")
        print(f"📧 Host : {settings.EMAIL_HOST}")
        
        # Envoi des emails de test
        emails_to_send = [
            (deposit_subject, deposit_message),
            (transfer_sent_subject, transfer_sent_message),
            (transfer_received_subject, transfer_received_message)
        ]
        
        for subject, message in emails_to_send:
            print(f"\n📤 Envoi : {subject}")
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                fail_silently=False
            )
            print(f"✅ Email envoyé : {subject}")
        
        print(f"\n🎉 Tous les emails de test ont été envoyés !")
        print(f"📬 Vérifiez votre boîte de réception : {test_email}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")
        print("\n🔧 Solutions possibles :")
        print("1. Vérifiez vos identifiants Gmail dans .env")
        print("2. Assurez-vous que l'authentification à 2 facteurs est activée")
        print("3. Vérifiez que l'App Password est correct")

if __name__ == "__main__":
    print("🧪 Test des emails de transactions PAYGUARD")
    print("=" * 60)
    test_transaction_emails()