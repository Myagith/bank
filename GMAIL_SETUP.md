# 📧 Configuration Gmail pour PAYGUARD

## 🎯 **Objectif**
Configurer PAYGUARD pour envoyer de vrais emails aux utilisateurs dans leur boîte mail.

---

## 🔧 **Étape 1 : Préparer votre compte Gmail**

### **1.1 Aller sur les paramètres de sécurité**
- Ouvrez : https://myaccount.google.com/security
- Connectez-vous avec votre compte Gmail

### **1.2 Activer l'authentification à 2 facteurs**
- Cliquez sur "Authentification à 2 facteurs"
- Suivez les étapes pour l'activer
- **IMPORTANT** : Cette étape est obligatoire

### **1.3 Créer un "App Password"**
- Retournez à la page de sécurité
- Cliquez sur "Mots de passe d'application"
- Sélectionnez "Mail" dans le menu déroulant
- Cliquez sur "Générer"
- **Copiez le mot de passe de 16 caractères** (ex: `abcd efgh ijkl mnop`)

---

## 🔧 **Étape 2 : Configurer le fichier .env**

### **2.1 Modifier le fichier .env**
Remplacez les valeurs dans le fichier `.env` :

```bash
# Remplacez par votre email Gmail
EMAIL_HOST_USER=votre.vrai.email@gmail.com

# Remplacez par votre App Password (16 caractères sans espaces)
EMAIL_HOST_PASSWORD=votre_app_password_16_caracteres

# Remplacez par votre email Gmail
DEFAULT_FROM_EMAIL=votre.vrai.email@gmail.com
```

### **2.2 Exemple de configuration**
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=monemail@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
EMAIL_USE_TLS=1
EMAIL_USE_SSL=0
DEFAULT_FROM_EMAIL=monemail@gmail.com
```

---

## 🧪 **Étape 3 : Tester la configuration**

### **3.1 Tester l'envoi d'email**
```bash
python3 test_email.py
```

### **3.2 Créer un utilisateur de test**
1. Connectez-vous en admin : `admin` / `Admin123!`
2. Allez dans "👥 Utilisateurs"
3. Cliquez sur "➕ Créer un utilisateur"
4. Remplissez le formulaire avec un email valide
5. Vérifiez que l'email est reçu

---

## 📧 **Types d'emails envoyés**

### **1. Email de bienvenue (création d'utilisateur)**
```
PAYGUARD - Vos identifiants de connexion

Bonjour {username},

Votre compte PAYGUARD a été créé avec succès.

🔐 Vos identifiants de connexion :
• Identifiant : {username}
• Mot de passe initial : {password}

⚠️ IMPORTANT : Changez votre mot de passe lors de votre première connexion.

🌐 Accédez à votre espace : http://localhost:8000/users/login/

Cordialement,
L'équipe PAYGUARD
```

### **2. Email OTP (connexion)**
```
PAYGUARD - Votre code de connexion sécurisé

Bonjour {username},

Votre code de connexion PAYGUARD est : {code}

Ce code expire dans {expires_minutes} minutes.

Si vous n'avez pas demandé ce code, ignorez cet email.

Cordialement,
L'équipe PAYGUARD
```

---

## 🔍 **Dépannage**

### **Erreur "Authentication failed"**
- ✅ Vérifiez que l'authentification à 2 facteurs est activée
- ✅ Vérifiez que l'App Password est correct
- ✅ Vérifiez que l'email est correct

### **Erreur "Connection refused"**
- ✅ Vérifiez votre connexion internet
- ✅ Vérifiez que le port 587 n'est pas bloqué

### **Emails dans les spams**
- ✅ Ajoutez votre email Gmail aux contacts
- ✅ Vérifiez le dossier spam

### **Erreur "Username and Password not accepted"**
- ✅ Utilisez l'App Password, pas votre mot de passe Gmail normal
- ✅ Vérifiez que l'App Password est copié correctement

---

## 🚀 **Alternative : Autres fournisseurs**

### **Outlook/Hotmail**
```bash
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
```

### **Yahoo**
```bash
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
```

---

## ✅ **Vérification**

Après configuration, vérifiez que :
- ✅ Les emails de bienvenue sont envoyés lors de la création d'utilisateur
- ✅ Les emails OTP sont envoyés lors de la connexion
- ✅ Les emails arrivent dans la boîte de réception (pas les spams)
- ✅ Le contenu des emails est correct

---

## 🎯 **Résultat final**

Quand un admin crée un utilisateur :
1. ✅ **Email de bienvenue** envoyé automatiquement
2. ✅ **Identifiants de connexion** inclus dans l'email
3. ✅ **Design professionnel** avec logo PAYGUARD
4. ✅ **Instructions claires** pour la première connexion

**L'utilisateur reçoit un vrai email dans sa boîte mail !** 🎉