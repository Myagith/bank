#!/usr/bin/env python3
"""
Script de test pour vérifier l'envoi d'emails réels
Usage: python3 test_real_email.py
"""

import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

def test_real_email():
    """Test l'envoi d'un email réel"""
    try:
        app_name = os.getenv('BANK_NAME', 'PAYGUARD')
        
        # Email de test
        test_email = input("Entrez votre email pour tester l'envoi réel : ").strip()
        if not test_email:
            print("❌ Email requis pour le test")
            return
        
        # Email de bienvenue de test
        welcome_subject = f"{app_name} - Test d'envoi d'email"
        welcome_message = f"""
Bonjour,

Ceci est un email de test pour vérifier que PAYGUARD peut envoyer de vrais emails.

🔐 Identifiants de test :
• Identifiant : test_user
• Mot de passe initial : Test123!

⚠️ IMPORTANT : Ceci est un test, ne vous connectez pas avec ces identifiants.

🌐 Accédez à votre espace : http://localhost:8000/users/login/

Cordialement,
L'équipe {app_name}
        """
        
        print(f"🔄 Envoi d'un email de test à : {test_email}")
        print(f"📧 Sujet : {welcome_subject}")
        print(f"📧 Backend : {settings.EMAIL_BACKEND}")
        print(f"📧 Host : {settings.EMAIL_HOST}")
        print(f"📧 Port : {settings.EMAIL_PORT}")
        print(f"📧 TLS : {settings.EMAIL_USE_TLS}")
        print(f"📧 From : {settings.DEFAULT_FROM_EMAIL}")
        
        # Envoi de l'email
        send_mail(
            subject=welcome_subject,
            message=welcome_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False
        )
        
        print("✅ Email envoyé avec succès !")
        print("📬 Vérifiez votre boîte de réception (et les spams)")
        print("🎉 Configuration Gmail réussie !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")
        print("\n🔧 Solutions possibles :")
        print("1. Vérifiez vos identifiants Gmail dans .env")
        print("2. Assurez-vous que l'authentification à 2 facteurs est activée")
        print("3. Vérifiez que l'App Password est correct")
        print("4. Vérifiez votre connexion internet")
        print("5. Consultez le guide GMAIL_SETUP.md")

if __name__ == "__main__":
    print("🧪 Test d'envoi d'email réel PAYGUARD")
    print("=" * 50)
    test_real_email()