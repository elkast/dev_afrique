#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Charger toutes les données initiales
python manage.py shell < donnees_initiales.py
python manage.py shell < donnees_lecons.py

# Créer le superuser
python manage.py creer_superuser
