import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── SECURITY ────────────────────────────────────────────────
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-!@l50ef+#dqgx)f+n+(wp1cx^w24_v(t&6)niqeuxmktfb8p*^'
)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*').split(',') if h.strip()]
# S'assurer que l'hôte Render est toujours inclus
if 'dev-afrique.onrender.com' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('dev-afrique.onrender.com')

# ─── APPS ────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'utilisateurs',
    'pages',
    'cours',
    'projets',
    'forum',
    'glossaire',
    'administration',
    'dmz',
]

# ─── MIDDLEWARE ───────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # DMZ Security middleware
    'dmz.middleware.PareFeuxMiddleware',
    'dmz.middleware.AdminProtectionMiddleware',
    'dmz.middleware.ExceptionNucleaireMiddleware',
]

ROOT_URLCONF = 'siteweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'siteweb.wsgi.application'

# ─── DATABASE ────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()
# Nettoyer channel_binding qui cause des erreurs avec dj-database-url
if 'channel_binding=' in DATABASE_URL:
    import re
    DATABASE_URL = re.sub(r'[&?]channel_binding=[^&]+', '', DATABASE_URL)

# Vérifier que DATABASE_URL a un schéma valide
VALID_SCHEMES = ('postgres://', 'postgresql://', 'sqlite://', 'mysql://', 'mysql2://')

DATABASES = {}
if DATABASE_URL and any(DATABASE_URL.startswith(scheme) for scheme in VALID_SCHEMES):
    # Configuration PostgreSQL avec options SSL pour Neon
    DATABASES = {
        'default': {
            **dj_database_url.parse(DATABASE_URL, conn_max_age=0),  # conn_max_age=0 pour Neon serverless
            'OPTIONS': {
                'sslmode': 'require',
                'connect_timeout': 10,
            }
        }
    }
else:
    # Fallback SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─── AUTH ────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'utilisateurs.Utilisateur'

# ─── I18N ────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# ─── STATIC & MEDIA ─────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 Mo
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

# ─── AUTH REDIRECTS ──────────────────────────────────────────
LOGIN_URL = '/utilisateurs/connexion/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── SECURITY HARDENING ─────────────────────────────────────
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    # Désactivé sur Render - le proxy gère déjà HTTPS
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    # Cookies sécurisés mais avec domaine flexible pour Render
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = None  # Permet les sous-domaines Render
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # CSRF trusted origins avec fallback Render
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]
    # Toujours inclure l'hôte Render
    if 'https://dev-afrique.onrender.com' not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append('https://dev-afrique.onrender.com')
else:
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 days
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ─── LOGGING ─────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'dmz': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ─── ADMIN SECURITY ─────────────────────────────────────────
# Required credentials for admin access
ADMIN_ALLOWED_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_ALLOWED_PASSWORD_HINT = os.environ.get('ADMIN_PASSWORD_HINT', '')
