from django.contrib import admin
from .models import Perfil
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        perfil, _ = Perfil.objects.get_or_create(user=obj)
        if perfil.es_admin:
            grupo_admin, _ = Group.objects.get_or_create(name='Admin')
            obj.groups.set([grupo_admin])
        else:
            grupo_usuario, _ = Group.objects.get_or_create(name='Usuario')
            obj.groups.set([grupo_usuario])
        perfil.save()

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Perfil)
