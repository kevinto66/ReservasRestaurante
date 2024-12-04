from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reservations.models import Usuario, Admin
from django.db import transaction


class Command(BaseCommand):
    help = 'Creates a superuser along with associated Usuario and Admin instances'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Create superuser if it doesn't exist
                if not User.objects.filter(username='admin').exists():
                    admin_user = User.objects.create_superuser(
                        username='admin',
                        email='admin@example.com',
                        password='admin123'
                    )

                    # Usuario and Admin instances will be created automatically by signals
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully created admin user'))
                else:
                    self.stdout.write(self.style.WARNING(
                        'Admin user already exists'))

                    # Ensure Usuario and Admin instances exist for existing superuser
                    admin_user = User.objects.get(username='admin')
                    usuario, created = Usuario.objects.get_or_create(
                        user=admin_user,
                        defaults={
                            'nombre_usuario': admin_user.username,
                            'correo': admin_user.email or 'admin@example.com',
                            'contrasenia': admin_user.password
                        }
                    )

                    Admin.objects.get_or_create(usuario=usuario)
