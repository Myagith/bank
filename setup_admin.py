#!/usr/bin/env python3
"""
Script pour configurer l'admin
Usage: python3 setup_admin.py
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

from users.models import User

def setup_admin():
    """Configurer l'admin avec le bon mot de passe et rôle"""
    
    print("🔧 Configuration de l'admin...")
    
    try:
        # Récupérer l'admin
        admin = User.objects.get(username='admin')
        
        # Définir le mot de passe
        admin.set_password('Admin123!')
        
        # Définir le rôle admin
        admin.role = User.Role.ADMIN
        admin.can_login = True
        
        # Sauvegarder
        admin.save()
        
        print("✅ Admin configuré avec succès !")
        print("   • Username: admin")
        print("   • Password: Admin123!")
        print("   • Role: ADMIN")
        print("   • Can login: True")
        
    except User.DoesNotExist:
        print("❌ L'utilisateur admin n'existe pas")
        print("   Créez d'abord un superutilisateur avec :")
        print("   python3 manage.py createsuperuser --username admin --email admin@example.com --noinput")
    except Exception as e:
        print(f"❌ Erreur lors de la configuration : {e}")

if __name__ == "__main__":
    setup_admin()