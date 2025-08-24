#!/usr/bin/env python3
"""
Script de test pour vérifier l'envoi d'emails
Usage: python3 test_email.py
"""

import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

def test_email_sending():
    """Test l'envoi d'un email de test"""
    try:
        # Test d'envoi d'email
        subject = "Test PAYGUARD - Configuration Email"
        message = """
Bonjour,

Ceci est un email de test pour vérifier la configuration SMTP de PAYGUARD.

Si vous recevez cet email, la configuration est correcte !

Cordialement,
L'équipe PAYGUARD
        """
        
        # Remplacer par votre email de test
        recipient_email = "test@example.com"
        
        print(f"🔄 Envoi d'un email de test à : {recipient_email}")
        print(f"📧 Sujet : {subject}")
        print(f"📧 Backend : {settings.EMAIL_BACKEND}")
        print(f"📧 Host : {settings.EMAIL_HOST}")
        print(f"📧 Port : {settings.EMAIL_PORT}")
        print(f"📧 TLS : {settings.EMAIL_USE_TLS}")
        print(f"📧 From : {settings.DEFAULT_FROM_EMAIL}")
        
        # Envoi de l'email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False
        )
        
        print("✅ Email envoyé avec succès !")
        print("📬 Vérifiez votre boîte de réception (et les spams)")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")
        print("\n🔧 Solutions possibles :")
        print("1. Vérifiez vos identifiants Gmail dans .env")
        print("2. Assurez-vous que l'authentification à 2 facteurs est activée")
        print("3. Vérifiez que l'App Password est correct")
        print("4. Testez avec un email valide")

if __name__ == "__main__":
    print("🧪 Test de configuration email PAYGUARD")
    print("=" * 50)
    
    # Demander l'email de test
    test_email = input("Entrez votre email pour le test (ou appuyez sur Entrée pour utiliser test@example.com) : ").strip()
    if not test_email:
        test_email = "test@example.com"
    
    # Mettre à jour l'email de test
    import sys
    sys.argv = [sys.argv[0]]  # Reset argv
    
    test_email_sending()