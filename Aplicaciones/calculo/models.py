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
        # Muestra capitalizado
        return self.nombre.capitalize()


# Class central
class Central(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    foto_central = models.FileField(upload_to='centrales', null=True, blank=True)
    empresa = models.CharField(max_length=100)
    tipo = models.CharField(max_length=200)
    potencia = models.FloatField()
    provincia = models.CharField(max_length=200)
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
    energia_anual_producida = models.FloatField(help_text="MWh/año", blank=True, null=True)
    energia_bruta_calculada = models.FloatField(editable=False, null=True, blank=True)

    factor_planta = models.FloatField(help_text="%")
    vida_util = models.FloatField(help_text="%")
    degradacion = models.FloatField(help_text="%")

    # Inversión
    inversion_total = models.FloatField(help_text="USD")
    porcentaje_capital_propio = models.FloatField(help_text="%", default=0.0)
    porcentaje_deuda = models.FloatField(help_text="%", default=0.0)
    capital_propio = models.FloatField(blank=True, null=True)
    deuda = models.FloatField(blank=True, null=True)

    # Financiación
    acreedor = models.CharField(max_length=100)
    tasa_interes_periodo = models.FloatField(help_text="%")
    periodos_por_anio = models.IntegerField()
    anios_pago_total = models.IntegerField()
    anios_gracia = models.IntegerField()

    tasa_interes_anual = models.FloatField(blank=True, null=True)
    total_periodos = models.IntegerField(blank=True, null=True)
    periodos_gracia = models.IntegerField(blank=True, null=True)
    periodos_pago = models.IntegerField(blank=True, null=True)
    anios_pago = models.FloatField(blank=True, null=True)

    # Costos
    costo_variable = models.FloatField(help_text="USD")
    costo_produccion = models.FloatField(help_text="USD")
    costo_anual_oma = models.FloatField(blank=True, null=True)
    costo_anual_oma_inversion = models.FloatField(blank=True, null=True)
    costo_anual_oma_mw = models.FloatField(blank=True, null=True)

    # Parámetros económicos para cálculo
    beta = models.FloatField(help_text="Coeficiente beta")
    margen_intermediacion = models.FloatField(help_text="%", default=0.0)
    inflacion = models.FloatField(help_text="%")
    economia = models.FloatField(help_text="%")
    riesgo = models.FloatField(help_text="Riesgo país", default=0.0)
    indice_premio = models.FloatField(blank=True, null=True)
    sin_riesgo = models.FloatField(help_text="% tasa sin riesgo", default=0.0)
    tasa_mercado = models.FloatField(help_text="% tasa mercado", default=0.0)
    premio_riesgo_mercado = models.FloatField(help_text="% premio riesgo mercado", default=0.0)
    impuesto = models.FloatField(help_text="% impuesto", default=0.0)

    def save(self, *args, **kwargs):
        # Energía producida
        if self.potencia_nominal and self.factor_planta:
            self.energia_anual_producida = self.potencia_nominal * (self.factor_planta / 100) * 8760
            self.energia_bruta_calculada = self.energia_anual_producida / 1000

        self.indice_premio = self.riesgo / 100
        # Capital y deuda
        self.capital_propio = self.inversion_total * (self.porcentaje_capital_propio / 100)
        self.deuda = self.inversion_total * (self.porcentaje_deuda / 100)

        # Financiación
        self.tasa_interes_anual = self.tasa_interes_periodo * self.periodos_por_anio
        self.total_periodos = self.periodos_por_anio * self.anios_pago_total
        self.periodos_gracia = self.periodos_por_anio * self.anios_gracia
        self.periodos_pago = self.total_periodos - self.periodos_gracia
        self.anios_pago = self.periodos_pago / self.periodos_por_anio if self.periodos_por_anio else 0

        # Costos
        self.costo_anual_oma = (self.inversion_total * 1.5) / 100
        self.costo_anual_oma_inversion = (self.costo_anual_oma * 100 / self.inversion_total) if self.inversion_total else 0
        self.costo_anual_oma_mw = self.costo_anual_oma / self.energia_anual_producida if self.energia_anual_producida else 0

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
    tipo_generacion = models.CharField(max_length=100, blank=True, null=True)  # Detectado automáticamente

    # Campos genéricos
    inversion_total = models.FloatField()
    energia_anual_producida = models.FloatField()
    vida_util = models.FloatField()
    tasa_descuento = models.FloatField()
    tasa_crecimiento_energia = models.FloatField(default=0.0)
    costo_operacion_anual = models.FloatField()

    capital_propio = models.FloatField(blank=True, null=True)
    deuda = models.FloatField(blank=True, null=True)
    porcentaje_capital_propio = models.FloatField(blank=True, null=True)
    porcentaje_deuda = models.FloatField(blank=True, null=True)

    # Interés y financiamiento
    tasa_interes_periodo = models.FloatField(blank=True, null=True)  # %
    tasa_interes_anual = models.FloatField(blank=True, null=True)    # %
    total_periodos = models.IntegerField(blank=True, null=True)
    anios_gracia = models.IntegerField(blank=True, null=True)
    periodos_pago = models.IntegerField(blank=True, null=True)

    # Costos
    costo_produccion = models.FloatField(blank=True, null=True)
    costo_variable = models.FloatField(blank=True, null=True)
    costo_anual_oma_mw = models.FloatField(blank=True, null=True)
    degradacion = models.FloatField(blank=True, null=True)

    # Datos financieros/económicos adicionales
    beta = models.FloatField(blank=True, null=True)
    impuesto = models.FloatField(blank=True, null=True)
    margen_intermediacion = models.FloatField(blank=True, null=True)
    inflacion = models.FloatField(blank=True, null=True)
    economia = models.FloatField(blank=True, null=True)
    riesgo = models.FloatField(blank=True, null=True)
    indice_premio = models.FloatField(blank=True, null=True)
    sin_riesgo = models.FloatField(blank=True, null=True)
    tasa_mercado = models.FloatField(blank=True, null=True)
    premio_riesgo_mercado = models.FloatField(blank=True, null=True)

    # Otros
    factor_planta = models.FloatField(blank=True, null=True)
    potencia_nominal = models.FloatField(blank=True, null=True)


    def calcular_lcoe(self):
        tipo = self.tipo_generacion.lower() if self.tipo_generacion else ""
        if tipo == "fotovoltaica":
            return self._calculo_fotovoltaico()
        else:
            return self._calculo_generico()

    def _calculo_generico(self):
        # Usar fórmula estándar
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

    def _calculo_fotovoltaico(self):
        try:
            # Valores base
            PN = self.potencia_nominal
            FP = self.factor_planta / 100
            VU = self.vida_util
            IN = self.inversion_total
            CP = self.capital_propio
            CV = self.costo_variable

            P_CP = (CP / IN)
            D = self.deuda
            P_D = (D / IN) 
            PDT = self.porcentaje_deuda / 100  
            TIP = self.tasa_interes_periodo / 100
            TIA = self.tasa_interes_anual / 100
            TP = self.total_periodos
            AG = self.anios_gracia
            PP = self.periodos_pago / 2 if self.periodos_pago else 0

            B = self.beta
            MB = self.margen_intermediacion / 100
            inflacion = self.inflacion / 100
            economia = self.economia / 100
            RP = self.riesgo
            IPR = self.indice_premio / 100
            TSR = self.sin_riesgo / 100
            TDM = self.tasa_mercado / 100
            PRM = self.premio_riesgo_mercado / 100 
            T = self.impuesto / 100
            EAP = self.energia_anual_producida

            cost_P = self.costo_produccion
            cost_an_p = self.costo_anual_oma_mw
            degradacion = self.degradacion / 100

            # Tasa minima aceptable
            tasa_minima = inflacion + IPR + (inflacion * IPR)

            # Beta de apalancamiento
            af1 = (P_D * (1 - T)) / P_CP
            B_AP = B * (1 + af1)
            
            # Costo cap propio
            af2 = (PRM * (B_AP /100))
            CT_CP = TSR + af2 + IPR
            
            # Tasa captacion
            tz_cp = ((1 + inflacion) * (1 + economia) - 1)
            CST_DEU = tz_cp + MB
            # wacc
            WACC = (((P_CP * CT_CP) + (P_D * CST_DEU)) / (P_CP + P_D))

            # Factor de Recuperacion de capital
            FRC = WACC * ((1 + WACC) ** VU) / ((1 + WACC) ** VU) 
            anualidad = D * FRC

            CF_total_1 = cost_P * EAP
            CF_total_2 = cost_an_p * EAP
            CF_total =  CF_total_1 + CF_total_2 
            CV_total = CV * EAP
            costos = CF_total + CV_total

            numerador = ((CP + costos) / ((1 + WACC) ** 1))

            denominador = ((EAP * ((1 + degradacion) ** 1)) / ((1 + WACC) ** 1))

            lcoe = round( numerador / denominador , 2)

            # Diccionario 
            return {
            'lcoe': round(lcoe, 4),  # LCOE puede ir con 4 decimales si deseas más precisión
            'PN': round(PN, 2), 'FP': round(FP, 2), 'VU': round(VU, 2), 'IN': round(IN, 2),
            'CP': round(CP, 2), 'CV': round(CV, 2), 'P_CP': round(P_CP, 2), 'D': round(D, 2),
            'P_D': round(P_D, 2), 'PDT': round(PDT, 2), 'TIP': round(TIP, 4), 'TIA': round(TIA, 4),
            'TP': round(TP, 2), 'AG': round(AG, 2), 'PP': round(PP, 2), 'B': round(B, 2),
            'MB': round(MB, 4), 'inflacion': round(inflacion, 4), 'economia': round(economia, 4),
            'RP': round(RP, 2), 'IPR': round(IPR, 4), 'TSR': round(TSR, 4), 'TDM': round(TDM, 4),
            'PRM': round(PRM, 4), 'T': round(T, 4), 'EAP': round(EAP, 2), 'cost_P': round(cost_P, 2),
            'cost_an_p': round(cost_an_p, 2), 'tasa_minima': round(tasa_minima, 4), 'af1': round(af1, 4),
            'B_AP': round(B_AP, 4), 'af2': round(af2, 4), 'CT_CP': round(CT_CP, 4),
            'tz_cp': round(tz_cp, 4), 'CST_DEU': round(CST_DEU, 4), 'WACC': round(WACC, 4),
            'degradacion': round(degradacion, 4), 'FRC': round(FRC, 4), 'anualidad': round(anualidad, 2),
            'CF_total': round(CF_total, 2), 'CV_total': round(CV_total, 2), 'costos': round(costos, 2),
            'numerador': round(numerador, 2), 'denominador': round(denominador, 2),
            'CF_total_1': round(CF_total_1, 2), 'CF_total_2': round(CF_total_2, 2)
        }
        except Exception as e:
            return {"error": str(e)}

class ResultadoCalculo(models.Model):
    caso = models.OneToOneField(CasoCalculo, on_delete=models.CASCADE)
    lcoe = models.FloatField(null=True, blank=True)
    fecha_calculo = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(null=True, blank=True)
    detalle = models.JSONField(null=True, blank=True)
                               
    def save(self, *args, **kwargs):
        try:
            parametros = self.caso.parametrocalculo
            if self.caso.central:
                tipo = self.caso.central.tipo_electrica.nombre.lower()
                parametros.tipo_generacion = tipo
                parametros.save()
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