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
echo "==> Initializing all data..."
python manage.py init_render

echo ""
echo "==> Running full diagnostic..."
python manage.py diagnostic_complet_render --fix

echo ""
echo "=========================================="
echo "BUILD COMPLETE"
echo "=========================================="
