from django.contrib import admin

from .models import TipoElectrica, Central, InformacionCentral, Fotovoltaica, CasoCalculo, ResultadoCalculo

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

@admin.register(Fotovoltaica)
class FotovoltaicaAdmin(admin.ModelAdmin):
    list_display = ('central', 'anio_ingreso', 'numero_paneles', 'sistema', 'potencia_nominal', 'potencia_efectiva', 'factor_planta')
    search_fields = ('central__nombre', 'sistema')
    list_filter = ('anio_ingreso',)

@admin.register(CasoCalculo)
class CasoCalculoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'usuario')  
    search_fields = ('nombre', 'usuario__username')
    list_filter = ('fecha',)  

@admin.register(ResultadoCalculo)
class ResultadoCalculoAdmin(admin.ModelAdmin):
    list_display = ('caso', 'lcoe', 'fecha_calculo')  
    search_fields = ('caso__nombre',)
    list_filter = ('fecha_calculo',)

