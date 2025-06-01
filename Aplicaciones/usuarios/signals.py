from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from .models import Perfil

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Usuario')

@receiver(post_save, sender=UserSocialAuth)
def asignar_grupo_usuario(sender, instance, created, **kwargs):
    if created:
        usuario = instance.user
        if not usuario.groups.exists():
            grupo = Group.objects.get(name='Usuario')
            usuario.groups.add(grupo)

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()