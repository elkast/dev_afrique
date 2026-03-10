#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit

echo "=========================================="
echo "STARTING BUILD"
echo "=========================================="

pip install -r requirements.txt

echo ""
echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo ""
echo "==> Running migrations..."
python manage.py migrate

echo ""
echo "==> Loading initial data..."
python manage.py shell < donnees_initiales.py || echo "Warning: donnees_initiales.py had issues"

echo ""
echo "==> Loading lessons data..."
python manage.py shell < donnees_lecons.py || echo "Warning: donnees_lecons.py had issues"

echo ""
echo "==> Creating superuser..."
python manage.py creer_superuser || echo "Warning: superuser creation had issues"

echo ""
echo "==> Verifying deployment..."
python manage.py verifier_deploiement || echo "Warning: verification had issues"

echo ""
echo "=========================================="
echo "BUILD COMPLETE"
echo "=========================================="
