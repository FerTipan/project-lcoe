from .models import ParametroCalculo, CasoCalculo, Fotovoltaica

def crear_parametros_desde_fotovoltaica(caso: CasoCalculo) -> ParametroCalculo:
    fotovoltaica = caso.central.fotovoltaica

    parametros = ParametroCalculo.objects.create(
        caso=caso,
        inversion_total=fotovoltaica.inversion_total,
        energia_anual_producida=fotovoltaica.energia_anual_producida,
        vida_util=fotovoltaica.vida_util,
        tasa_descuento=0.08, 
        tasa_crecimiento_energia=0.0,
        costo_operacion_anual=fotovoltaica.costo_anual_oma
    )
    return parametros
