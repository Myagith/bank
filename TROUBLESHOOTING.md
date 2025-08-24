# 🔧 Guide de Dépannage PAYGUARD

## 🚨 **Problème : Redirection vers l'admin Django au lieu du dashboard**

### **Symptôme :**
Après saisie de l'OTP, vous êtes redirigé vers `/admin/` au lieu du dashboard PAYGUARD.

### **Cause :**
L'utilisateur `admin` n'a pas le bon rôle dans le modèle personnalisé.

---

## 🔧 **Solutions :**

### **Solution 1 : Script automatique**
```bash
python3 fix_admin_role.py
```

### **Solution 2 : Manuel via Django shell**
```bash
python3 manage.py shell
```

```python
from users.models import User
admin_user = User.objects.get(username='admin')
admin_user.role = User.Role.ADMIN
admin_user.can_login = True
admin_user.save()
print(f"Rôle corrigé: {admin_user.role}")
```

### **Solution 3 : Via l'admin Django**
1. Allez sur `http://localhost:8000/admin/`
2. Connectez-vous avec `admin` / `Admin123!`
3. Allez dans "Users" → "Users"
4. Cliquez sur l'utilisateur "admin"
5. Changez "Role" vers "Admin"
6. Sauvegardez

---

## 🔍 **Vérification :**

### **Test de connexion :**
1. Allez sur `http://localhost:8000/users/login/`
2. Connectez-vous avec `admin` / `Admin123!`
3. Saisissez l'OTP : `123456`
4. Vous devriez être redirigé vers le dashboard admin

### **URLs attendues :**
- ✅ **Dashboard Admin** : `http://localhost:8000/dashboard/admin/`
- ✅ **Dashboard Client** : `http://localhost:8000/dashboard/client/`
- ❌ **Admin Django** : `http://localhost:8000/admin/` (ne devrait pas être la redirection)

---

## 🐛 **Debug :**

### **Vérifier les logs du serveur :**
Quand vous vous connectez, vous devriez voir dans les logs :
```
DEBUG: User admin has role: ADMIN
DEBUG: User is_superuser: True
DEBUG: User is_admin property: True
DEBUG: Redirecting to admin dashboard
```

### **Vérifier la base de données :**
```bash
python3 manage.py shell
```

```python
from users.models import User
admin = User.objects.get(username='admin')
print(f"Username: {admin.username}")
print(f"Role: {admin.role}")
print(f"Is superuser: {admin.is_superuser}")
print(f"Can login: {admin.can_login}")
```

---

## 🚀 **Prévention :**

### **Créer un admin correct dès le début :**
```bash
python3 manage.py shell
```

```python
from users.models import User
from django.contrib.auth.hashers import make_password

# Créer un admin avec le bon rôle
admin = User.objects.create(
    username='admin',
    email='admin@payguard.com',
    password=make_password('Admin123!'),
    role=User.Role.ADMIN,
    can_login=True,
    is_superuser=True,
    is_staff=True
)
print("Admin créé avec succès!")
```

---

## 📋 **Checklist de résolution :**

- [ ] L'utilisateur `admin` existe
- [ ] Le rôle est défini sur `ADMIN`
- [ ] `can_login` est `True`
- [ ] `is_superuser` est `True`
- [ ] Les URLs du dashboard sont correctes
- [ ] Le serveur redémarre après modification

---

## 🆘 **Si le problème persiste :**

### **Vérifier les URLs :**
```python
# Dans users/views.py, ligne ~75
if user.role == User.Role.ADMIN or user.is_superuser:
    return redirect('dashboard:admin')  # Vérifier que cette URL existe
```

### **Vérifier les permissions :**
```python
# Dans dashboard/views.py
@login_required
def dashboard_admin(request):
    # Vérifier que cette vue est accessible
```

### **Redémarrer le serveur :**
```bash
# Arrêter le serveur (Ctrl+C)
python3 manage.py runserver 0.0.0.0:8000
```

---

## ✅ **Résultat attendu :**

Après correction, la connexion devrait :
1. ✅ Accepter `admin` / `Admin123!`
2. ✅ Demander l'OTP `123456`
3. ✅ Rediriger vers `/dashboard/admin/`
4. ✅ Afficher le dashboard avec tous les graphiques
5. ✅ Permettre l'accès à la gestion des utilisateurs