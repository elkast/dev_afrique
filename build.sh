#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# RÉINITIALISATION COMPLÈTE - supprime et recrée tout
python reinitialiser_neon.py

# Vérification
python manage.py verifier_deploiement

echo ""
echo "============================================"
echo "BUILD TERMINÉ"
echo "============================================"
