# Déploiement Django sur Render + Neon

Tutoriel complet pour déployer une application Django avec PostgreSQL sur Neon et Render.

---

## 📋 Prérequis

- Compte GitHub
- Compte Render (render.com)
- Compte Neon (neon.tech)
- Projet Django fonctionnel en local

---

## Étape 1 : Base de données Neon

### 1.1 Créer un projet
1. Connectez-vous sur [neon.tech](https://neon.tech)
2. Cliquez **"New Project"**
3. Nom : `devafrique-db`
4. Région : `US East (N. Virginia)` (plus proche de Render)
5. Cliquez **"Create Project"**

### 1.2 Récupérer l'URL de connexion
1. Dans le dashboard Neon, cliquez **"Connect"**
2. Sélectionnez **"PostgreSQL"**
3. Copiez l'URL complète :
```
postgres://user:password@host:port/database?sslmode=require
```

**Conservez cette URL, elle sera utilisée dans Render.**

---

## Étape 2 : Préparer le projet Django

### 2.1 Fichier requirements.txt
```
django>=4.2,<5.0
dj-database-url>=2.0
psycopg2-binary>=2.9
gunicorn>=21.0
whitenoise>=6.0
python-dotenv>=1.0
```

### 2.2 Configuration settings.py
```python
import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# === SECURITE ===
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-key-change-in-prod')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
host = os.environ.get('ALLOWED_HOSTS', '')
if host:
    ALLOWED_HOSTS.extend(host.split(','))

# === BASE DE DONNEES ===
DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()
VALID_SCHEMES = ('postgres://', 'postgresql://')

if DATABASE_URL and any(DATABASE_URL.startswith(s) for s in VALID_SCHEMES):
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}

# === STATIQUES ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajoutez ceci
    # ... autres middlewares
]

# === CSRF (pour HTTPS) ===
CSRF_TRUSTED_ORIGINS = []
csrf_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if csrf_origins:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins.split(',') if o.strip()]
```

### 2.3 Fichier build.sh (racine du projet)
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Rendez exécutable : `chmod +x build.sh`

### 2.4 Fichier render.yaml (racine du projet)
```yaml
services:
  - type: web
    name: devafrique
    runtime: python
    plan: free
    buildCommand: "./build.sh"
    startCommand: "gunicorn siteweb.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: DJANGO_DEBUG
        value: "False"
      - key: ALLOWED_HOSTS
        value: "votre-app.onrender.com,.onrender.com"
      - key: DATABASE_URL
        value: "postgresql://neon-user:password@neon-host/neondb?sslmode=require"
      - key: CSRF_TRUSTED_ORIGINS
        value: "https://votre-app.onrender.com"
      - key: PYTHON_VERSION
        value: "3.12.0"
```

**Remplacez** `votre-app` et l'URL Neon par vos valeurs réelles.

### 2.5 Fichier .gitignore
```
.venv/
__pycache__/
*.pyc
.env
db.sqlite3
staticfiles/
media/
```

---

## Étape 3 : Déploiement sur Render

### 3.1 Créer le service web
1. Connectez-vous sur [render.com](https://render.com)
2. Dashboard → **"New +"** → **"Web Service"**
3. Connectez votre repo GitHub
4. Sélectionnez le repository

### 3.2 Configuration
| Champ | Valeur |
|-------|--------|
| Name | `devafrique` |
| Region | `Oregon (US West)` |
| Branch | `main` |
| Runtime | `Python 3` |
| Build Command | `./build.sh` |
| Start Command | `gunicorn siteweb.wsgi:application --bind 0.0.0.0:$PORT` |

### 3.3 Variables d'environnement
Ajoutez dans l'onglet **Environment** :

| Key | Value |
|-----|-------|
| `DJANGO_SECRET_KEY` | Générer une clé sécurisée |
| `DJANGO_DEBUG` | `False` |
| `ALLOWED_HOSTS` | `devafrique.onrender.com,.onrender.com` |
| `DATABASE_URL` | URL Neon complète |
| `CSRF_TRUSTED_ORIGINS` | `https://devafrique.onrender.com` |

### 3.4 Déployer
1. Cliquez **"Create Web Service"**
2. Render déploie automatiquement
3. Surveillez les logs dans l'onglet **Logs**

---

## Étape 4 : Créer le superutilisateur

### 4.1 Commande shell sur Render
1. Dashboard → votre service → **"Shell"**
2. Exécutez :
```bash
cd /opt/render/project/src
python manage.py createsuperuser
```

### 4.2 Alternative : commande automatisée
Créez `utilisateurs/management/commands/creer_superuser.py` :
```python
from django.core.management.base import BaseCommand
from utilisateurs.models import Utilisateur
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        
        if not Utilisateur.objects.filter(username=username).exists():
            Utilisateur.objects.create_superuser(
                username=username, email=email, password=password,
                first_name='Admin', last_name='System', role='administrateur'
            )
            self.stdout.write(self.style.SUCCESS(f'Admin {username} créé'))
```

Ajoutez dans `build.sh` :
```bash
python manage.py creer_superuser
```

Ajoutez dans `render.yaml` :
```yaml
      - key: ADMIN_USERNAME
        value: "admin"
      - key: ADMIN_PASSWORD
        value: "VotreMotDePasseSecurise123!"
      - key: ADMIN_EMAIL
        value: "admin@votresite.com"
```

---

## Étape 5 : Vérifier le déploiement

### 5.1 Tests à effectuer
| URL | Résultat attendu |
|-----|------------------|
| `https://votre-app.onrender.com/` | Page d'accueil |
| `https://votre-app.onrender.com/admin/` | Page admin Django |
| `https://votre-app.onrender.com/administration/` | Votre admin personnalisé |

### 5.2 Commandes de debug
Si erreur 502 ou 400, vérifiez les logs Render :
```
==> Build
==> Running 'gunicorn siteweb.wsgi:application'
[ERROR] DisallowedHost: Invalid HTTP_HOST header
```

Corrections communes :
- **502** : Erreur Python → vérifiez `ALLOWED_HOSTS`
- **400** : Mauvais host → ajoutez le domaine Render à `ALLOWED_HOSTS`

---

## 🔄 Workflow de mise à jour

### Pousser un changement
```bash
git add .
git commit -m "Description du changement"
git push origin main
```

Render déploie automatiquement.

### Base de données
Neon persiste les données. Les migrations s'exécutent à chaque build via `build.sh`.

---

## 🛠️ Dépannage

### Erreur "UnknownSchemeError"
**Cause** : `DATABASE_URL` vide ou invalide
**Fix** : Vérifiez la variable dans Render Environment

### Erreur "DisallowedHost"
**Cause** : Domaine non dans `ALLOWED_HOSTS`
**Fix** : Ajoutez `votre-app.onrender.com` dans les variables d'env

### Erreur 502 Bad Gateway
**Cause** : Gunicorn crash
**Fix** : Vérifiez les logs Render, corrigez l'erreur Python

### Static files 404
**Cause** : Whitenoise mal configuré
**Fix** : Vérifiez `MIDDLEWARE` et `STORAGES` dans settings.py

---

## 📁 Structure finale

```
devafrique/
├── build.sh              # Script de build Render
├── render.yaml           # Configuration Render
├── requirements.txt      # Dépendances
├── manage.py
├── siteweb/
│   ├── settings.py       # Config avec dj_database_url
│   ├── wsgi.py
│   └── urls.py
├── utilisateurs/
│   └── management/
│       └── commands/
│           └── creer_superuser.py
└── static/
```

---

## ✅ Checklist pré-déploiement

- [ ] `DEBUG = False` en production
- [ ] `SECRET_KEY` générée et sécurisée
- [ ] `ALLOWED_HOSTS` contient le domaine Render
- [ ] `DATABASE_URL` configurée avec URL Neon
- [ ] `build.sh` est exécutable
- [ ] `render.yaml` présent
- [ ] `.gitignore` exclut `.env` et `db.sqlite3`
- [ ] Whitenoise configuré pour les statics
- [ ] Migrations testées en local

---

## 🚀 Ressources

- [Render Docs](https://render.com/docs)
- [Neon Docs](https://neon.tech/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
