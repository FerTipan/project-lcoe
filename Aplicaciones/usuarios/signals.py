from django.contrib.auth.models import Group, User
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth
from .models import Perfil

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Usuario')

@receiver(post_save, sender=UserSocialAuth)
def asignar_grupo_y_perfil_usuario_social(sender, instance, created, **kwargs):
    if created:
        usuario = instance.user

        # Asignar al grupo Usuario si no tiene grupo
        if not usuario.groups.exists():
            grupo = Group.objects.get(name='Usuario')
            usuario.groups.add(grupo)

        # Crear o actualizar el perfil
        Perfil.objects.get_or_create(user=usuario, defaults={'es_admin': False})

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil_usuario(sender, instance, **kwargs):
    Perfil.objects.get_or_create(user=instance)
