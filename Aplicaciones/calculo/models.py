from django.db import models
from Aplicaciones.usuarios.models import Perfil
from decimal import Decimal

# Class TipoGeneracion 
class TipoElectrica(models.Model):
    nombre = models.CharField(max_length=100)
    foto_tipo = models.FileField(upload_to='tipo_electrica', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.strip().upper() 
        super().save(*args, **kwargs)
    
    def __str__(self):
        # Muestra capitalizado
        return self.nombre.capitalize()


# Class central
class Central(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    foto_central = models.FileField(upload_to='centrales', null=True, blank=True)
    empresa = models.CharField(max_length=100)
    tipo = models.CharField(max_length=200)
    potencia = models.DecimalField(max_digits=15, decimal_places=6, help_text="MW")
    provincia = models.CharField(max_length=200)
    anio_operacion = models.PositiveIntegerField()
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
    potencia_nominal = models.DecimalField(max_digits=15, decimal_places=6, help_text="MW")
    potencia_efectiva = models.DecimalField(max_digits=15, decimal_places=6, help_text="MWp")
    # Energía
    energia_anual_producida = models.DecimalField(max_digits=20, decimal_places=4, help_text="MWh/año", blank=True, null=True)
    energia_bruta_calculada = models.DecimalField(max_digits=20, decimal_places=4, editable=False, null=True, blank=True)

    factor_planta = models.DecimalField(max_digits=10, decimal_places=4, help_text="%")
    vida_util = models.IntegerField(help_text="años")
    degradacion = models.DecimalField(max_digits=10, decimal_places=4, help_text="%")

    # Inversión
    inversion_total = models.DecimalField(max_digits=20, decimal_places=2, help_text="USD")
    porcentaje_capital_propio = models.DecimalField(max_digits=10, decimal_places=4, help_text="%", default=0.0)
    porcentaje_deuda = models.DecimalField(max_digits=10, decimal_places=4, help_text="%", default=0.0)
    capital_propio = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    deuda = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # Financiación
    acreedor = models.CharField(max_length=100)
    tasa_interes_periodo = models.DecimalField(max_digits=10, decimal_places=4, help_text="%")
    periodos_por_anio = models.IntegerField()
    anios_pago_total = models.IntegerField()
    anios_gracia = models.IntegerField()

    tasa_interes_anual = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    total_periodos = models.IntegerField(blank=True, null=True)
    periodos_gracia = models.IntegerField(blank=True, null=True)
    periodos_pago = models.IntegerField(blank=True, null=True)
    anios_pago = models.IntegerField(blank=True, null=True)

    # Costos
    costo_variable = models.DecimalField(max_digits=15, decimal_places=6, help_text="USD")
    costo_produccion = models.DecimalField(max_digits=15, decimal_places=6, help_text="USD")
    costo_anual_oma = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    costo_anual_oma_inversion = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    costo_anual_oma_mw = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    
    # Parámetros económicos para cálculo
    beta = models.DecimalField(max_digits=10, decimal_places=4, help_text="Coeficiente beta")
    margen_intermediacion = models.DecimalField(max_digits=10, decimal_places=4, help_text="%", default=0.0)
    inflacion = models.DecimalField(max_digits=10, decimal_places=4, help_text="%")
    economia = models.DecimalField(max_digits=10, decimal_places=4, help_text="%")
    riesgo = models.DecimalField(max_digits=10, decimal_places=4, help_text="Riesgo país", default=0.0)
    indice_premio = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    sin_riesgo = models.DecimalField(max_digits=10, decimal_places=4, help_text="% tasa sin riesgo", default=0.0)
    tasa_mercado = models.DecimalField(max_digits=10, decimal_places=4, help_text="% tasa mercado", default=0.0)
    premio_riesgo_mercado = models.DecimalField(max_digits=10, decimal_places=4, help_text="% premio riesgo mercado", default=0.0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=4, help_text="% impuesto", default=0.0)
    
    def save(self, *args, **kwargs):
        if self.potencia_nominal and self.factor_planta:
            self.energia_anual_producida = self.potencia_nominal * (self.factor_planta / Decimal('100')) * Decimal('8760')
            self.energia_bruta_calculada = self.energia_anual_producida / Decimal('1000')

        self.indice_premio = self.riesgo / Decimal('100') if self.riesgo else None
        self.capital_propio = self.inversion_total * (self.porcentaje_capital_propio / Decimal('100')) if self.inversion_total else None
        self.deuda = self.inversion_total * (self.porcentaje_deuda / Decimal('100')) if self.inversion_total else None

        self.tasa_interes_anual = self.tasa_interes_periodo * self.periodos_por_anio
        self.total_periodos = self.periodos_por_anio * self.anios_pago_total
        self.periodos_gracia = self.periodos_por_anio * self.anios_gracia
        self.periodos_pago = self.total_periodos - self.periodos_gracia
        self.anios_pago = self.periodos_pago / self.periodos_por_anio if self.periodos_por_anio else None

        self.costo_anual_oma = (self.inversion_total * Decimal('0.015')) if self.inversion_total else None
        self.costo_anual_oma_inversion = (self.costo_anual_oma * Decimal('100') / self.inversion_total) if self.inversion_total else None
        self.costo_anual_oma_mw = (self.costo_anual_oma / self.energia_anual_producida) if self.energia_anual_producida else None

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

class ParametroCalculos(models.Model):
    caso = models.OneToOneField(CasoCalculo, on_delete=models.CASCADE)
    tipo_generacion = models.CharField(max_length=100, blank=True, null=True)

    # Campos genéricos
    inversion_total = models.DecimalField(max_digits=20, decimal_places=2)
    energia_anual_producida = models.DecimalField(max_digits=20, decimal_places=4)
    vida_util = models.IntegerField()
    tasa_descuento = models.DecimalField(max_digits=10, decimal_places=4)
    tasa_crecimiento_energia = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    costo_operacion_anual = models.DecimalField(max_digits=20, decimal_places=2)

    capital_propio = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    deuda = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    porcentaje_capital_propio = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    porcentaje_deuda = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    degradacion = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    # Datos financieros/económicos adicionales
    beta = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    impuesto = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    margen_intermediacion = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    inflacion = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    economia = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    riesgo = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    indice_premio = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    sin_riesgo = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    tasa_mercado = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    premio_riesgo_mercado = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    
    # Otros
    factor_planta = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    potencia_nominal = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    # Interés y financiamiento
    tasa_interes_periodo = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    tasa_interes_anual = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    total_periodos = models.IntegerField(blank=True, null=True)
    anios_gracia = models.IntegerField(blank=True, null=True)
    periodos_pago = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True

class ParametroFotovoltaica(ParametroCalculos):
    # Costos
    costo_produccion = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    costo_variable = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    costo_anual_oma_mw = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    def calcular_lcoe(self):
        try:
            # Conversión segura con Decimal
            PN = Decimal(self.potencia_nominal or 0)
            FP = Decimal(self.factor_planta or 0) / Decimal('100')
            VU = Decimal(self.vida_util or 0)
            IN = Decimal(self.inversion_total or 0)
            CP = Decimal(self.capital_propio or 0)
            CV = Decimal(self.costo_variable or 0)

            P_CP = (CP / IN) if IN else Decimal('0')
            D = Decimal(self.deuda or 0)
            P_D = (D / IN) if IN else Decimal('0')
            PDT = Decimal(self.porcentaje_deuda or 0) / Decimal('100')
            TIP = Decimal(self.tasa_interes_periodo or 0) / Decimal('100')
            TIA = Decimal(self.tasa_interes_anual or 0) / Decimal('100')
            TP = Decimal(self.total_periodos or 0)
            AG = Decimal(self.anios_gracia or 0)
            PP = Decimal(self.periodos_pago or 0) / Decimal('2')

            B = Decimal(self.beta or 0)
            MB = Decimal(self.margen_intermediacion or 0) / Decimal('100')
            inflacion = Decimal(self.inflacion or 0) / Decimal('100')
            economia = Decimal(self.economia or 0) / Decimal('100')
            RP = Decimal(self.riesgo or 0)
            IPR = Decimal(self.indice_premio or 0) / Decimal('100')
            TSR = Decimal(self.sin_riesgo or 0) / Decimal('100')
            TDM = Decimal(self.tasa_mercado or 0) / Decimal('100')
            PRM = Decimal(self.premio_riesgo_mercado or 0) / Decimal('100')
            T = Decimal(self.impuesto or 0) / Decimal('100')
            EAP = Decimal(self.energia_anual_producida or 0)

            cost_P = Decimal(self.costo_produccion or 0)
            cost_an_p = Decimal(self.costo_anual_oma_mw or 0)
            degradacion = Decimal(self.degradacion or 0) / Decimal('100')

            # Tasa minima 
            tasa_minima = inflacion + IPR + (inflacion * IPR)

            # Ajuste de beta con apalancamiento financiero
            af1 = (P_D * (1 - T)) / P_CP if P_CP else Decimal('0')
            B_AP = B * (1 + af1)
            CT_CP = TSR + (PRM * (B_AP / Decimal('100'))) + IPR

            # Costo deuda
            tz_cp = ((1 + inflacion) * (1 + economia) - 1)
            CST_DEU = tz_cp + MB

            # WACC (costo promedio ponderado de capital)
            WACC = ((P_CP * CT_CP) + (P_D * CST_DEU)) / (P_CP + P_D) if (P_CP + P_D) else Decimal('0')
            WACC = WACC.quantize(Decimal('0.0001'))

            # Anualidad de la deuda 
            FRC = WACC * ((1 + WACC) ** VU) / (((1 + WACC) ** VU) - 1) if VU and WACC else Decimal('0')
            anualidad = D * FRC

            # Costos totales
            CF_total_1 = cost_P * EAP
            CF_total_2 = cost_an_p * EAP
            CF_total = CF_total_1 + CF_total_2
            CV_total = CV * EAP
            costos = CF_total + CV_total

            # Año base t = 1
            t = 1
            numerador = CP + (costos / ((1 + WACC) ** t)) if WACC else CP + costos
            denominador = (EAP * ((1 - degradacion) ** t)) / ((1 + WACC) ** t) if WACC else EAP

            lcoe = numerador / denominador if denominador else None
            return lcoe.quantize(Decimal('0.0001')) if lcoe else None

        except Exception as e:
            return {"error": str(e)}
        
    class ParametroGenerico(ParametroCalculos):

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
                return round(numerador / denominador, 4)
            except Exception:
                return None


class ResultadoCalculo(models.Model):
    caso = models.OneToOneField(CasoCalculo, on_delete=models.CASCADE)
    lcoe = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
    fecha_calculo = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(null=True, blank=True)
                               
    def save(self, *args, **kwargs):
        try:
            parametros = None
            tipo = None
            if hasattr(self.caso, 'parametrofotovoltaica'):
                parametros = self.caso.parametrofotovoltaica
                tipo = 'fotovoltaica'
            elif hasattr(self.caso, 'parametrogenerico'):
                parametros = self.caso.parametrogenerico
                tipo = 'genérico'
            #  elif para otras tecnologías

            if parametros:
                self.lcoe = parametros.calcular_lcoe()
                parametros.tipo_generacion = tipo
                parametros.save()
            else:
                self.lcoe = None
        except Exception:
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