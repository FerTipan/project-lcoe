from django.contrib import admin

from .models import TipoElectrica, Central, InformacionCentral

@admin.register(TipoElectrica)
class TipoElectricaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Central)
class CentralAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(InformacionCentral)
class InformacionCentralAdmin(admin.ModelAdmin):
    list_display = ('capacidad',)
