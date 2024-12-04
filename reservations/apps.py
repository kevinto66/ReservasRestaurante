from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'

    def ready(self):
        import reservations.signals  # Import signals when app is ready

        # Create Usuario for existing superusers if needed
        from django.contrib.auth.models import User
        from .models import Usuario, Admin

        for user in User.objects.filter(is_superuser=True):
            if not hasattr(user, 'usuario'):
                usuario, created = Usuario.objects.get_or_create(
                    user=user,
                    defaults={
                        'nombre_usuario': user.username,
                        'correo': user.email or f"{user.username}@example.com",
                        'contrasenia': user.password
                    }
                )
                if created:
                    Admin.objects.get_or_create(usuario=usuario)
