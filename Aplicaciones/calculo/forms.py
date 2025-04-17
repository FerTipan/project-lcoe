from django import forms
from .models import TipoElectrica, Central, InformacionCentral

class TipoElectricaForm(forms.ModelForm):
    class Meta:
        model = TipoElectrica
        fields = ['nombre']

class CentralForm(forms.ModelForm):
    class Meta:
        model = Central
        fields = [
            'nombre', 'ubicacion', 'empresa', 'tipo', 'potencia', 'e_media',
            'provincia', 'canton', 'anio_operacion', 'tipo_electrica'
        ]

class InformacionCentralForm(forms.ModelForm):
    class Meta:
        model = InformacionCentral
        fields = [
            'capacidad', 'vida_util', 'inversion', 'factor_planta', 'anio', 'central'
        ]
