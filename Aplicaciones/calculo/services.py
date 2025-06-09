from .models import ParametroCalculo, CasoCalculo, Fotovoltaica

def crear_parametros_desde_tipo_generacion(caso: CasoCalculo) -> ParametroCalculo | None:
    if not caso.central or not caso.central.tipo_electrica:
        return None

    tipo = caso.central.tipo_electrica.nombre.strip().lower()

    if tipo == 'fotovoltaica':
        return crear_parametros_desde_fotovoltaica(caso)

    '''agregando más tecnologías
    elif tipo == 'hidroeléctrica':
        return crear_parametros_desde_hidroelectrica(caso)

    elif tipo == 'eólica':
        return crear_parametros_desde_eolica(caso)'''

    return None

def crear_parametros_desde_fotovoltaica(caso: CasoCalculo) -> ParametroCalculo:
    fotovoltaica = caso.central.fotovoltaica

    parametros = ParametroCalculo.objects.create(
        caso=caso,
        tipo_generacion='Fotovoltaica',

        # --- Datos base ---
        inversion_total=fotovoltaica.inversion_total,
        energia_anual_producida=fotovoltaica.energia_anual_producida,
        vida_util=fotovoltaica.vida_util,
        tasa_descuento=0.08,  
        tasa_crecimiento_energia=0.0,
        costo_operacion_anual=fotovoltaica.costo_anual_oma,

        # --- Fotovoltaica ---
        potencia_nominal=fotovoltaica.potencia_nominal,
        capital_propio=fotovoltaica.capital_propio,
        deuda=fotovoltaica.deuda,
        porcentaje_capital_propio=fotovoltaica.porcentaje_capital_propio,
        porcentaje_deuda=fotovoltaica.porcentaje_deuda,

        tasa_interes_periodo=fotovoltaica.tasa_interes_periodo,
        tasa_interes_anual=fotovoltaica.tasa_interes_anual,
        total_periodos=fotovoltaica.total_periodos,
        anios_gracia=fotovoltaica.anios_gracia,
        periodos_pago=fotovoltaica.periodos_pago,

        costo_produccion=fotovoltaica.costo_produccion,
        costo_variable=fotovoltaica.costo_variable,
        costo_anual_oma_mw=fotovoltaica.costo_anual_oma_mw,
        degradacion = fotovoltaica.degradacion,
        beta=fotovoltaica.beta,
        impuesto=fotovoltaica.impuesto,
        sin_riesgo=fotovoltaica.sin_riesgo,
        inflacion=fotovoltaica.inflacion,
        economia=fotovoltaica.economia,
        margen_intermediacion=fotovoltaica.margen_intermediacion,
        indice_premio=fotovoltaica.indice_premio,
        premio_riesgo_mercado=fotovoltaica.premio_riesgo_mercado,
        tasa_mercado=fotovoltaica.tasa_mercado,
        riesgo=fotovoltaica.riesgo,
        factor_planta=fotovoltaica.factor_planta
    )

    return parametros

