from django.db import models
from Aplicaciones.usuarios.models import Perfil

# Class TipoGeneracion 
class TipoElectrica(models.Model):
    nombre = models.CharField(max_length=100)
    foto_tipo = models.FileField(upload_to='tipo_electrica', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.strip().upper() 
        super().save(*args, **kwargs)
    
    def __str__(self):
        # Muestra capitalizado (solo visual)
        return self.nombre.capitalize()


# Class central
class Central(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    foto_central = models.FileField(upload_to='centrales', null=True, blank=True)
    empresa = models.CharField(max_length=100)
    tipo = models.CharField(max_length=200)
    potencia = models.FloatField()
    e_media = models.FloatField()
    provincia = models.CharField(max_length=200)
    canton = models.CharField(max_length=200)
    anio_operacion = models.CharField(max_length=200)
    tipo_electrica = models.ForeignKey(
        TipoElectrica,
        on_delete=models.CASCADE,
        related_name='centrales'
    )

    def __str__(self):
        return self.nombre

class Fotovoltaica(models.Model):
    central = models.OneToOneField('Central', on_delete=models.CASCADE, related_name='fotovoltaica')

    anio_ingreso = models.PositiveIntegerField()
    numero_paneles = models.IntegerField()
    sistema = models.CharField(max_length=100)

    # Potencias
    potencia_nominal = models.FloatField(help_text="MW")
    potencia_efectiva = models.FloatField(help_text="MWp")

    # Energías
    energia_anual_producida = models.FloatField(help_text="MWh/año")

    # Calculado: energía_bruta = energia_anual_producida / 1000
    energia_bruta_calculada = models.FloatField(editable=False, null=True, blank=True)

    factor_planta = models.FloatField(help_text="%")
    vida_util = models.FloatField(help_text="%")
    degradacion = models.FloatField(help_text="%")

    # Inversión
    inversion_total = models.FloatField(help_text="USD")
    capital_propio = models.FloatField(help_text="USD")

    # Financiación
    acreedor = models.CharField(max_length=100)
    deuda = models.FloatField(help_text="USD")
    tasa_interes_anual = models.FloatField(help_text="%")
    tasa_interes_periodo = models.FloatField(help_text="%")
    periodos_por_anio = models.IntegerField()
    anios_pago_total = models.IntegerField()
    total_periodos = models.IntegerField()
    anios_gracia = models.IntegerField()
    periodos_gracia = models.IntegerField()
    periodos_pago = models.IntegerField()
    anios_pago = models.IntegerField()

    # Costos
    costo_variable = models.FloatField(help_text="USD")
    costo_produccion = models.FloatField(help_text="USD")
    costo_anual_oma = models.FloatField(help_text="USD")
    costo_anual_oma_inversion = models.FloatField(help_text="%")
    costo_anual_oma_mw = models.FloatField(help_text="USD/MW-año")

    def save(self, *args, **kwargs):
        # Calcular energía bruta sino está definido manualmente
        if self.energia_anual_producida:
            self.energia_bruta_calculada = self.energia_anual_producida / 1000
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Fotovoltaica: {self.central.nombre}'

class CasoCalculo(models.Model):
    nombre = models.CharField(max_length=200)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    central = models.ForeignKey('Central', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    es_simulacion = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} - {self.fecha.date()}'

class ParametroCalculo(models.Model):
    caso = models.OneToOneField(CasoCalculo, on_delete=models.CASCADE)
    inversion_total = models.FloatField()
    energia_anual_producida = models.FloatField()
    vida_util = models.FloatField()
    tasa_descuento = models.FloatField()
    tasa_crecimiento_energia = models.FloatField(default=0.0)
    costo_operacion_anual = models.FloatField()

    def calcular_lcoe(self):
        try:
            r = self.tasa_descuento
            d = self.tasa_crecimiento_energia
            n = int(self.vida_util)
            energia_anual = self.energia_anual_producida
            costo_operacion = self.costo_operacion_anual
            inversion = self.inversion_total

            numerador = inversion
            denominador = 0

            for t in range(1, n + 1):
                numerador += costo_operacion / ((1 + r) ** t)
                energia_t = energia_anual * ((1 + d) ** t)
                denominador += energia_t / ((1 + r) ** t)

            if denominador == 0:
                return None

            lcoe = numerador / denominador
            return round(lcoe, 4)
        except Exception:
            return None


class ResultadoCalculo(models.Model):
    caso = models.OneToOneField(CasoCalculo, on_delete=models.CASCADE)
    lcoe = models.FloatField()
    fecha_calculo = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            parametros = self.caso.parametrocalculo
            self.lcoe = parametros.calcular_lcoe()
        except ParametroCalculo.DoesNotExist:
            self.lcoe = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resultado - {self.caso.nombre}"

# Class Info Central
class InformacionCentral(models.Model):
    capacidad = models.FloatField()
    vida_util = models.IntegerField()
    inversion = models.FloatField()
    factor_planta = models.FloatField()
    anio = models.CharField(max_length=200)
    central = models.ForeignKey(
        Central,
        on_delete=models.CASCADE,
        related_name='informaciones'
    )

    def __str__(self):
        return f"{self.central.nombre} - {self.anio}"