from django.core.management.base import BaseCommand
from utilisateurs.models import Utilisateur
import os

class Command(BaseCommand):
    help = 'Crée un superutilisateur admin pour Render'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        email = os.environ.get('ADMIN_EMAIL', 'admin@devafrique.com')
        
        if not Utilisateur.objects.filter(username=username).exists():
            user = Utilisateur.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='System',
                role='administrateur'  # Rôle admin requis
            )
            self.stdout.write(self.style.SUCCESS(f'Admin "{username}" créé avec rôle administrateur'))
        else:
            user = Utilisateur.objects.get(username=username)
            if user.role != 'administrateur':
                user.role = 'administrateur'
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Rôle de "{username}" mis à jour : administrateur'))
            else:
                self.stdout.write(self.style.WARNING(f'Admin "{username}" existe déjà'))
