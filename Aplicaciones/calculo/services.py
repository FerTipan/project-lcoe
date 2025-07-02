import unicodedata
from .models import ParametroFotovoltaica, CasoCalculo, ParametroTermica
from typing import Union
ParametroGenerico = Union[ParametroFotovoltaica, ParametroTermica]

def quitar_tildes(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def crear_parametros_desde_tipo_generacion(caso: CasoCalculo) -> ParametroGenerico | None:
    if not caso.central or not caso.central.tipo_electrica:
        return None

    tipo = caso.central.tipo_electrica.nombre.strip().lower()

    if tipo == 'fotovoltaica':
        return crear_parametros_desde_fotovoltaica(caso)
    elif tipo == 'termica':
        return crear_parametros_desde_termica(caso)
    '''elif tipo == 'eólica':
        return crear_parametros_desde_eolica(caso)
    elif tipo == 'hidroeléctrica':
        return crear_parametros_desde_hidroelectrica(caso) '''

    return None

def crear_parametros_desde_fotovoltaica(caso: CasoCalculo) -> ParametroFotovoltaica:
    fotovoltaica = caso.central.fotovoltaica

    parametros = ParametroFotovoltaica.objects.create(  # usa la subclase concreta
        caso=caso,
        tipo_generacion='Fotovoltaica',
        inversion_total=fotovoltaica.inversion_total,
        energia_anual_producida=fotovoltaica.energia_anual_producida,
        vida_util=fotovoltaica.vida_util,
        tasa_descuento=0.08,  
        tasa_crecimiento_energia=0.0,
        capital_propio=fotovoltaica.capital_propio,
        deuda=fotovoltaica.deuda,
        porcentaje_capital_propio=fotovoltaica.porcentaje_capital_propio,
        porcentaje_deuda=fotovoltaica.porcentaje_deuda,
        degradacion = fotovoltaica.degradacion,
        beta=fotovoltaica.beta,
        impuesto=fotovoltaica.impuesto,
        margen_intermediacion=fotovoltaica.margen_intermediacion,
        inflacion=fotovoltaica.inflacion,
        economia=fotovoltaica.economia,
        riesgo=fotovoltaica.riesgo,
        indice_premio=fotovoltaica.indice_premio,
        sin_riesgo=fotovoltaica.sin_riesgo,
        tasa_mercado=fotovoltaica.tasa_mercado,
        premio_riesgo_mercado=fotovoltaica.premio_riesgo_mercado,
        factor_planta=fotovoltaica.factor_planta,
        potencia_nominal=fotovoltaica.potencia_nominal,
        tasa_interes_periodo=fotovoltaica.tasa_interes_periodo,
        tasa_interes_anual=fotovoltaica.tasa_interes_anual,
        total_periodos=fotovoltaica.total_periodos,
        anios_gracia=fotovoltaica.anios_gracia,
        periodos_pago=fotovoltaica.periodos_pago,
        # Costos específicos de fotovoltaica
        costo_produccion=fotovoltaica.costo_produccion,
        costo_variable=fotovoltaica.costo_variable,
        costo_anual_oma_mw=fotovoltaica.costo_anual_oma_mw,
    )
    return parametros

# ----------------------------------- TERMICA ----------------------------
def crear_parametros_desde_termica(caso: CasoCalculo) -> ParametroTermica:
    termica = caso.central.termica

    parametros = ParametroTermica.objects.create(
        caso=caso,
        tipo_generacion='Termica',
        inversion_total=termica.inversion_total,
        energia_anual_producida=termica.energia_anual_producida,
        vida_util=termica.vida_util,
        tasa_descuento=0.08,
        tasa_crecimiento_energia=0.0,
        potencia_nominal=termica.potencia_nominal,
        capital_propio=termica.capital_propio,
        deuda=termica.deuda,
        porcentaje_capital_propio=termica.porcentaje_capital_propio,
        porcentaje_deuda=termica.porcentaje_deuda,
        degradacion=termica.degradacion,
        beta=termica.beta,
        impuesto=termica.impuesto,
        margen_intermediacion=termica.margen_intermediacion,
        inflacion=termica.inflacion,
        economia=termica.economia,
        riesgo=termica.riesgo,
        indice_premio=termica.indice_premio,
        sin_riesgo=termica.sin_riesgo,
        tasa_mercado=termica.tasa_mercado,
        premio_riesgo_mercado=termica.premio_riesgo_mercado,
        factor_planta=termica.factor_planta,
        tasa_interes_periodo=termica.tasa_interes_periodo,
        tasa_interes_anual=termica.tasa_interes_anual,
        total_periodos=termica.total_periodos,
        anios_gracia=termica.anios_gracia,
        periodos_pago=termica.periodos_pago,
        # Costos de O&M
        costo_produccion=termica.costo_produccion,
        porcentaje_oma=termica.porcentaje_oma,
        costo_oma=termica.costo_oma,
        costo_oma_usd=termica.costo_oma_usd,
        # Administración
        gastos_administracion=termica.gastos_administracion,
        pt_unidad_negocio=termica.pt_unidad_negocio,
        costo_administracion=termica.costo_administracion,
        # Combustibles
        usd_galon=termica.usd_galon,
        gal_anio=termica.gal_anio,
        usd_cb_total=termica.usd_cb_total,
        # Costos operativos
        transporte=termica.transporte,
        lub_quim=termica.lub_quim,
        agua_p=termica.agua_p,
        mantenimiento_oim_moam=termica.mantenimiento_oim_moam,
        ctrl_amb=termica.ctrl_amb,
        srv_aux=termica.srv_aux,
    )

    return parametros