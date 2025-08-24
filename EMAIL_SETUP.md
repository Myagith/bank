# 📧 Configuration Email PAYGUARD

## 🎯 Objectif
Configurer PAYGUARD pour envoyer de vrais emails aux utilisateurs lors de leur création et pour les codes OTP.

## 🔧 Configuration Gmail (Recommandé)

### Étape 1 : Préparer votre compte Gmail

1. **Allez sur** : https://myaccount.google.com/security
2. **Activez l'authentification à 2 facteurs** si ce n'est pas déjà fait
3. **Créez un "App Password"** :
   - Cliquez sur "Mots de passe d'application"
   - Sélectionnez "Mail" dans le menu déroulant
   - Cliquez sur "Générer"
   - **Copiez le mot de passe de 16 caractères** (ex: `abcd efgh ijkl mnop`)

### Étape 2 : Configurer le fichier .env

Modifiez le fichier `.env` avec vos informations :

```bash
# Remplacez par votre email Gmail
EMAIL_HOST_USER=votre.email@gmail.com

# Remplacez par votre App Password (16 caractères sans espaces)
EMAIL_HOST_PASSWORD=votre_app_password_ici

# Remplacez par votre email Gmail
DEFAULT_FROM_EMAIL=votre.email@gmail.com
```

### Étape 3 : Tester la configuration

```bash
# Lancer le test d'email
python3 test_email.py
```

## 📧 Types d'emails envoyés

### 1. Email de bienvenue (création d'utilisateur)
- **Quand** : Admin crée un nouvel utilisateur
- **Contenu** : Identifiants de connexion
- **Destinataire** : L'utilisateur créé

### 2. Email OTP (connexion)
- **Quand** : Utilisateur se connecte
- **Contenu** : Code à 6 chiffres
- **Destinataire** : L'utilisateur qui se connecte

## 🔍 Dépannage

### Erreur "Authentication failed"
- ✅ Vérifiez que l'authentification à 2 facteurs est activée
- ✅ Vérifiez que l'App Password est correct
- ✅ Vérifiez que l'email est correct

### Erreur "Connection refused"
- ✅ Vérifiez votre connexion internet
- ✅ Vérifiez que le port 587 n'est pas bloqué

### Emails dans les spams
- ✅ Ajoutez votre email Gmail aux contacts
- ✅ Vérifiez le dossier spam

## 🚀 Alternative : Autres fournisseurs

### Outlook/Hotmail
```bash
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
```

### Yahoo
```bash
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
```

## 📱 Test rapide

1. **Configurez votre .env** avec vos identifiants Gmail
2. **Lancez le test** : `python3 test_email.py`
3. **Créez un utilisateur** via l'interface admin
4. **Vérifiez** que l'email de bienvenue est reçu

## ✅ Vérification

Après configuration, quand un admin crée un utilisateur :
- ✅ Email de bienvenue envoyé automatiquement
- ✅ Identifiants inclus dans l'email
- ✅ Design professionnel avec le logo PAYGUARD
- ✅ Instructions de connexion claires