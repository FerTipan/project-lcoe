from django.contrib import admin

from .models import TipoElectrica, Central, CentralTermica, CentralFotovoltaica, InformacionCentral

@admin.register(TipoElectrica)
class TipoElectricaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Central)
class CentralAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(CentralTermica)
class TermicaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costos_produccion', 'costos_om', 'costos_administracion')
    search_fields = ('nombre',)
    list_filter = ('costos_produccion',)

@admin.register(CentralFotovoltaica)
class CentralFotovoltaicaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costos_prod')
    search_fields = ('nombre',)

@admin.register(InformacionCentral)
class InformacionCentralAdmin(admin.ModelAdmin):
    list_display = ('capacidad',)
