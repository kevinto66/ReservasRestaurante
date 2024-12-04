from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Usuario, Admin


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create Usuario and Admin instances when a User is created
    """
    if created or not hasattr(instance, 'usuario'):
        # Create Usuario for any user (including superuser) if it doesn't exist
        usuario, created = Usuario.objects.get_or_create(
            user=instance,
            defaults={
                'nombre_usuario': instance.username,
                'correo': instance.email or f"{instance.username}@example.com",
                'contrasenia': instance.password
            }
        )

        # Create Admin instance for superuser if it doesn't exist
        if instance.is_superuser and not hasattr(usuario, 'admin'):
            Admin.objects.get_or_create(usuario=usuario)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to update Usuario instance when User is updated
    """
    if hasattr(instance, 'usuario'):
        instance.usuario.nombre_usuario = instance.username
        instance.usuario.correo = instance.email or f"{instance.username}@example.com"
        instance.usuario.save()
