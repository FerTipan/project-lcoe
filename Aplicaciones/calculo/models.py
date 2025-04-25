from django.db import models

# Class TipoGeneracion 
class TipoElectrica(models.Model):
    nombre = models.CharField(max_length=100)
    foto_tipo = models.FileField(upload_to='tipo_electrica', null=True, blank=True)

    def __str__(self):
        return self.nombre

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

# Class CentralTermica
class CentralTermica(Central):
    costos_produccion = models.FloatField()
    costos_om = models.FloatField()
    costos_administracion = models.FloatField()

    costos_combustible = models.FloatField()
    costos_transporte = models.FloatField()
    costos_lubricacion = models.FloatField()
    costo_agua = models.FloatField()
    costo_mantenimeinto = models.FloatField()
    costo_control_ambiental = models.FloatField()
    costo_servicios_auxiliares = models.FloatField()

    def to_dict(self):
        return {
            "tipo": "Térmica",
            "costos_produccion": self.costos_produccion,
            "costos_om": self.costos_om,
            "costos_administracion": self.costos_administracion,
            "costos_combustible": self.costos_combustible,
            "costos_transporte": self.costos_transporte,
            "costos_lubricacion": self.costos_lubricacion,
            "costo_agua": self.costo_agua,
            "costo_mantenimeinto": self.costo_mantenimeinto,
            "costo_control_ambiental": self.costo_control_ambiental,
            "costo_servicios_auxiliares": self.costo_servicios_auxiliares,
        }

class CentralFotovoltaica(Central):
    costos_prod = models.FloatField()
    costos_om = models.FloatField()

    costos_var = models.FloatField()
    
    def to_dict(self):
        return {
            "tipo": "Fotovoltaica",
            "costos_produccion": self.costos_produccion,
            "costos_om": self.costos_om,
            "costos_variable": self.costos_variable,
        }

 
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