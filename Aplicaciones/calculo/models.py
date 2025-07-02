from django.db import models
from Aplicaciones.usuarios.models import Perfil
from decimal import Decimal

# -----------------------------  Class TipoGeneracion -----------------------------
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

# ----------------------------- Class Central ------------------------------------
class Central(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    foto_central = models.FileField(upload_to='centrales', null=True, blank=True)
    empresa = models.CharField(max_length=100)
    tipo = models.CharField(max_length=200)
    potencia = models.DecimalField(max_digits=15, decimal_places=6, help_text="MW")
    provincia = models.CharField(max_length=200)
    anio_operacion = models.CharField()
    tipo_electrica = models.ForeignKey(
        TipoElectrica,
        on_delete=models.CASCADE,
        related_name='centrales'
    )

    def __str__(self):
        return self.nombre

# ----------------------------- Class Fotovoltaica --------------------------------
class Fotovoltaica(models.Model):
    central = models.OneToOneField('Central', on_delete=models.CASCADE, related_name='fotovoltaica')

    anio_ingreso = models.CharField()
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


# ----------------------------- Class Termica --------------------------------
class Termica(models.Model):
    central = models.OneToOneField('Central', on_delete=models.CASCADE, related_name='termica')
    anio_instalacion = models.CharField(max_length=10)

    # Potencias
    potencia_nominal = models.DecimalField(max_digits=15, decimal_places=6, help_text="MW")
    potencia_efectiva = models.DecimalField(max_digits=15, decimal_places=6, help_text="MW")
    # Energias
    energia_anual_producida = models.DecimalField(max_digits=20, decimal_places=4, help_text="MWh/año", blank=True, null=True)
    energia_bruta_calculada = models.DecimalField(max_digits=20, decimal_places=4, help_text="GWh", editable=False, blank=True, null=True)
    
    factor_planta = models.DecimalField(max_digits=10, decimal_places=4, help_text="%")
    tipo_turbina = models.CharField(max_length=100)
    n_turbina = models.IntegerField()
    vida_util = models.IntegerField(help_text="años")
    degradacion = models.DecimalField(max_digits=10, decimal_places=4, help_text="%")

    # Inversión
    inversion_total = models.DecimalField(max_digits=20, decimal_places=2, help_text="USD")
    porcentaje_capital_propio = models.DecimalField(max_digits=10, decimal_places=4, help_text="%", default=0.0)
    porcentaje_deuda = models.DecimalField(max_digits=10, decimal_places=4, help_text="%", default=0.0)
    capital_propio = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    deuda = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    # Financiamiento
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

    # Costos de O&M
    costo_produccion = models.DecimalField(max_digits=15, decimal_places=6, help_text="USD")
    porcentaje_oma = models.DecimalField(max_digits=10, decimal_places=4, help_text="%", default=0.0)
    costo_oma = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    costo_oma_usd = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    # Administración
    gastos_administracion = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD")
    pt_unidad_negocio = models.DecimalField(max_digits=10, decimal_places=4, help_text="%")
    costo_administracion = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    # CV: Combustibles
    tp_combustible_a = models.CharField(max_length=100)
    usd_galon = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD/galon")
    gal_anio = models.DecimalField(max_digits=10, decimal_places=4, help_text="GAL/a")
    tp_combustible_p = models.CharField(max_length=100)
    usd_galon_1 = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD")
    gal_anio_1 = models.DecimalField(max_digits=10, decimal_places=4, help_text="GAL/a")
    usd_cb_total = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    # costos operativos
    transporte = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD")
    lub_quim = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD")
    agua_p = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD")
    mantenimiento_oim_moam = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD")
    ctrl_amb = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD")
    srv_aux = models.DecimalField(max_digits=10, decimal_places=4, help_text="USD")

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

        # Financiamiento
        self.capital_propio = self.inversion_total * (self.porcentaje_capital_propio / Decimal('100')) if self.inversion_total else None
        self.deuda = self.inversion_total * (self.porcentaje_deuda / Decimal('100')) if self.inversion_total else None
        self.tasa_interes_anual = self.tasa_interes_periodo * self.periodos_por_anio
        self.total_periodos = self.periodos_por_anio * self.anios_pago_total
        self.periodos_gracia = self.periodos_por_anio * self.anios_gracia
        self.periodos_pago = self.total_periodos - self.periodos_gracia
        self.anios_pago = self.periodos_pago / self.periodos_por_anio if self.periodos_por_anio else None

        self.indice_premio = self.riesgo / Decimal('100') if self.riesgo else None
        # Costo O&M
        if self.inversion_total:
            self.costo_oma = self.inversion_total * (self.porcentaje_oma / Decimal('100'))
            self.costo_oma_usd = (self.costo_oma / self.energia_anual_producida) if self.energia_anual_producida else None

        # Costo de administración
        self.costo_administracion = (self.gastos_administracion * ((self.potencia_nominal / self.pt_unidad_negocio))) / self.energia_anual_producida

        # Costo total de combustibles
        self.usd_cb_total = ((self.usd_galon * self.gal_anio) + (self.usd_galon_1 * self.gal_anio_1)) / self.energia_anual_producida

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Térmica: {self.central.nombre}'

# ----------------------------- Class Caso Calculo --------------------------------
class CasoCalculo(models.Model):
    nombre = models.CharField(max_length=200)
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    central = models.ForeignKey('Central', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    es_simulacion = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} - {self.fecha.date()}'

# ------------------------------- Class Paramentros de Calculo --------------------------------
class ParametroCalculos(models.Model):
    caso = models.OneToOneField(CasoCalculo, on_delete=models.CASCADE)
    tipo_generacion = models.CharField(max_length=100, blank=True, null=True)

    # Campos genéricos
    inversion_total = models.DecimalField(max_digits=20, decimal_places=2)
    energia_anual_producida = models.DecimalField(max_digits=20, decimal_places=4)
    vida_util = models.IntegerField()
    tasa_descuento = models.DecimalField(max_digits=10, decimal_places=4)
    tasa_crecimiento_energia = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    #costo_operacion_anual = models.DecimalField(max_digits=20, decimal_places=2)

    capital_propio = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    deuda = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    porcentaje_capital_propio = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    porcentaje_deuda = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    degradacion = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    # Datos financieros/económicos
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

# ------------------------------ Class Parametro Fotovoltaica -------------------------------------
class ParametroFotovoltaica(ParametroCalculos):
    # Costos
    costo_produccion = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    costo_variable = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    costo_anual_oma_mw = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    def calcular_lcoe(self):
        from decimal import Decimal, getcontext
        getcontext().prec = 40
        try:
            # Conversión a Decimal
            def to_decimal(val):
                return Decimal(str(val)) if val is not None else Decimal('0')

            PN = to_decimal(self.potencia_nominal)
            FP = to_decimal(self.factor_planta) / Decimal('100')
            VU = to_decimal(self.vida_util)
            IN = to_decimal(self.inversion_total)
            CP = to_decimal(self.capital_propio)
            CV = to_decimal(self.costo_variable)

            P_CP = (CP / IN) if IN else Decimal('0')
            D = to_decimal(self.deuda)
            P_D = (D / IN) if IN else Decimal('0')
            PDT = to_decimal(self.porcentaje_deuda) / Decimal('100')
            TIP = to_decimal(self.tasa_interes_periodo) / Decimal('100')
            TIA = to_decimal(self.tasa_interes_anual) / Decimal('100')
            TP = to_decimal(self.total_periodos)
            AG = to_decimal(self.anios_gracia)
            PP = to_decimal(self.periodos_pago) / Decimal('2') if self.periodos_pago else Decimal('0')

            B = to_decimal(self.beta)
            MB = to_decimal(self.margen_intermediacion) / Decimal('100')
            inflacion = to_decimal(self.inflacion) / Decimal('100')
            economia = to_decimal(self.economia) / Decimal('100')
            RP = to_decimal(self.riesgo)
            IPR = to_decimal(self.indice_premio) / Decimal('100')
            TSR = to_decimal(self.sin_riesgo) / Decimal('100')
            TDM = to_decimal(self.tasa_mercado) / Decimal('100')
            PRM = to_decimal(self.premio_riesgo_mercado) / Decimal('100')
            T = to_decimal(self.impuesto) / Decimal('100')
            EAP = to_decimal(self.energia_anual_producida)

            cost_P = to_decimal(self.costo_produccion)
            cost_an_p = to_decimal(self.costo_anual_oma_mw)
            degradacion = to_decimal(self.degradacion) / Decimal('100')

            # Tasa minima 
            tasa_minima = inflacion + IPR + (inflacion * IPR)

            # Ajuste beta con apalancamiento financiero
            af1 = (P_D * (1 - T)) / P_CP if P_CP else Decimal('0')
            B_AP = B * (1 + af1)
            CT_CP = TSR + (PRM * (B_AP / Decimal('100'))) + IPR

            # Costo deuda
            tz_cp = ((1 + inflacion) * (1 + economia) - 1)
            CST_DEU = tz_cp + MB

            # WACC
            WACC = ((P_CP * CT_CP) + (P_D * CST_DEU)) / (P_CP + P_D) if (P_CP + P_D) else Decimal('0')

            # Anualidad de la deuda 
            FRC = WACC * ((1 + WACC) ** VU) / (((1 + WACC) ** VU) - 1) if VU and WACC else Decimal('0')
            anualidad = D * FRC

            # Costos totales
            CF_total_1 = cost_P * EAP
            CF_total_2 = cost_an_p * EAP
            CF_total = CF_total_1 + CF_total_2
            # Costo variable total
            CV_total = CV * EAP
            # Suma de costos 
            costos = CF_total + CV_total

            # Año base t = 1
            t = Decimal('1')

            # Fórmula unificada para lcoe
            if WACC != 0 and EAP != 0:
                lcoe =((CP)+((costos)/(1+WACC)**1))/((EAP*(1+degradacion)**1))/((1+WACC)**1)
            else:
                lcoe = None

            #  prints
            print("Potencia nominal:", PN)
            print("Factor planta:", FP)
            print("Energia Anual Producida:", EAP)
            print("WACC:", WACC)
            print("Anualidad:", anualidad)
            print("Costos:", costos)
            print("LCOE:", lcoe)

            return lcoe.quantize(Decimal('0.0001')) if lcoe else None

        except Exception as e:
            return {"error": str(e)}
        
# ----------------------------- Class Parametro Térmica ----------------------------------
class ParametroTermica(ParametroCalculos):
    # Costos de O&M
    costo_produccion = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    porcentaje_oma = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    costo_oma = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    costo_oma_usd = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    # Administración
    gastos_administracion = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    pt_unidad_negocio = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    costo_administracion = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)

    # CV: Combustibles
    usd_galon = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    gal_anio = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    #tp_combustible_p = models.CharField(max_length=100)
    #usd_galon_1 = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    #gal_anio_1 = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    usd_cb_total = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)

    # costos operativos
    transporte = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    lub_quim = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    agua_p = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    mantenimiento_oim_moam = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    ctrl_amb = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    srv_aux = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)

    def calcular_lcoe(self):
        from decimal import Decimal, getcontext
        getcontext().prec = 40
        try:
            # Conversión a Decimal
            def to_decimal(val):
                return Decimal(str(val)) if val is not None else Decimal('0')

            PN = to_decimal(self.potencia_nominal)
            FP = to_decimal(self.factor_planta) / Decimal('100')
            VU = to_decimal(self.vida_util)
            IN = to_decimal(self.inversion_total)
            CP = to_decimal(self.capital_propio)

            P_CP = (CP / IN) if IN else Decimal('0')
            D = to_decimal(self.deuda)
            P_D = (D / IN) if IN else Decimal('0')
            PDT = to_decimal(self.porcentaje_deuda) / Decimal('100')
            TIP = to_decimal(self.tasa_interes_periodo) / Decimal('100')
            TIA = to_decimal(self.tasa_interes_anual) / Decimal('100')
            TP = to_decimal(self.total_periodos)
            AG = to_decimal(self.anios_gracia)
            PP = to_decimal(self.periodos_pago) / Decimal('2') if self.periodos_pago else Decimal('0')

            B = to_decimal(self.beta)
            MB = to_decimal(self.margen_intermediacion) / Decimal('100')
            inflacion = to_decimal(self.inflacion) / Decimal('100')
            economia = to_decimal(self.economia) / Decimal('100')
            RP = to_decimal(self.riesgo)
            IPR = to_decimal(self.indice_premio) / Decimal('100')
            TSR = to_decimal(self.sin_riesgo) / Decimal('100')
            TDM = to_decimal(self.tasa_mercado) / Decimal('100')
            PRM = to_decimal(self.premio_riesgo_mercado) / Decimal('100')
            T = to_decimal(self.impuesto) / Decimal('100')
            EAP = to_decimal(self.energia_anual_producida)

            cost_P = to_decimal(self.costo_produccion)
            degradacion = to_decimal(self.degradacion) / Decimal('100')
            # costos
            porcentaje_oma = to_decimal(self.porcentaje_oma) / Decimal('100')
            costo_oma = to_decimal(self.costo_oma)
            costo_oma_usd = to_decimal(self.costo_oma_usd)

            gastos_administracion = to_decimal(self.gastos_administracion)
            pt_unidad_negocio = to_decimal(self.pt_unidad_negocio)
            
            #Gastos admin
            costo_administracion = to_decimal(self.costo_administracion)
            usd_cb_total = to_decimal(self.usd_cb_total)
            transporte = to_decimal(self.transporte)
            lub_quim = to_decimal(self.lub_quim)
            agua_p = to_decimal(self.agua_p)
            mantenimiento_oim_moam = to_decimal(self.mantenimiento_oim_moam)
            ctrl_amb = to_decimal(self.ctrl_amb)
            srv_aux = to_decimal(self.srv_aux)
            
            # Tasa minima 
            tasa_minima = inflacion + IPR + (inflacion * IPR)

            # Ajuste beta con apalancamiento financiero
            af1 = (P_D * (1 - T)) / P_CP if P_CP else Decimal('0')
            B_AP = B * (1 + af1)
            CT_CP = TSR + (PRM * (B_AP / Decimal('100'))) + IPR

            # Costo deuda
            tz_cp = ((1 + inflacion) * (1 + economia) - 1)
            CST_DEU = tz_cp + MB

            # WACC
            WACC = ((P_CP * CT_CP) + (P_D * CST_DEU)) / (P_CP + P_D) if (P_CP + P_D) else Decimal('0')

            # Anualidad de la deuda 
            FRC = WACC * ((1 + WACC) ** VU) / (((1 + WACC) ** VU) - 1) if VU and WACC else Decimal('0')
            anualidad = D * FRC

            # Costos Fijos totales
            CF_total_1 = cost_P * EAP
            CF_total_2 = costo_oma_usd * EAP
            CF_total_3 = costo_administracion * EAP
            CF_total = CF_total_1 + CF_total_2 + CF_total_3

            # Costo variable total
            CV_1 = usd_cb_total * EAP
            CV_2 = transporte * EAP
            CV_3 = lub_quim * EAP
            CV_4 = agua_p * EAP
            CV_5 = mantenimiento_oim_moam * EAP
            CV_6 = ctrl_amb * EAP
            CV_7 = srv_aux * EAP
            CV_total = CV_1 + CV_2 + CV_3 + CV_4 + CV_5 + CV_6 + CV_7

            # Suma de costos 
            costos = CF_total + CV_total

            # Año base t = 1
            t = Decimal('1')

            # Fórmula unificada para lcoe
            if WACC != 0 and EAP != 0:
                lcoe =((CP)+((costos)/(1+WACC)**1))/((EAP*(1+degradacion)**1))/((1+WACC)**1)
            else:
                lcoe = None

            #  prints
            print("Potencia nominal:", PN)
            print("Factor planta:", FP)
            print("Energia Anual Producida:", EAP)
            print("COMBUSTIBLE:" , usd_cb_total)
            print("WACC:", WACC)
            print("Anualidad:", anualidad)
            print("Costos:", costos)
            print("LCOE:", lcoe)

            return lcoe.quantize(Decimal('0.0001')) if lcoe else None

        except Exception as e:
            return {"error": str(e)}
# ----------------------------- Class Parametro Eólica ------------------------------------


# ----------------------------- Class Parametro Hidráulica --------------------------------



# ----------------------------- Class Resultados Cálculo ----------------------------------
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
            elif hasattr(self.caso, 'parametrotermica'):
                parametros = self.caso.parametrotermica
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

# ----------------------------- Fin Class --------------------------------

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