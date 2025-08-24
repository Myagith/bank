#!/usr/bin/env python3
"""
Script pour corriger le rôle de l'utilisateur admin
Usage: python3 fix_admin_role.py
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

from users.models import User

def fix_admin_role():
    """Corrige le rôle de l'utilisateur admin"""
    try:
        # Récupérer l'utilisateur admin
        admin_user = User.objects.get(username='admin')
        
        print(f"🔍 Utilisateur trouvé: {admin_user.username}")
        print(f"📊 Rôle actuel: {admin_user.role}")
        print(f"👑 Superuser: {admin_user.is_superuser}")
        print(f"🔐 Can login: {admin_user.can_login}")
        
        # Corriger le rôle si nécessaire
        if admin_user.role != User.Role.ADMIN:
            admin_user.role = User.Role.ADMIN
            admin_user.can_login = True
            admin_user.save(update_fields=['role', 'can_login'])
            print(f"✅ Rôle corrigé: {admin_user.role}")
        else:
            print(f"✅ Rôle déjà correct: {admin_user.role}")
        
        # Vérifier la correction
        admin_user.refresh_from_db()
        print(f"🎯 Rôle final: {admin_user.role}")
        print(f"🎯 Propriété is_admin: {admin_user.is_admin}")
        
    except User.DoesNotExist:
        print("❌ Utilisateur 'admin' non trouvé")
        print("💡 Créez-le avec: python3 manage.py createsuperuser")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔧 Correction du rôle admin PAYGUARD")
    print("=" * 50)
    fix_admin_role()