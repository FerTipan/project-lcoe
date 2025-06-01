from django import forms
from .models import TipoElectrica, Central, InformacionCentral, Fotovoltaica

class TipoElectricaForm(forms.ModelForm):
    class Meta:
        model = TipoElectrica
        fields = ['nombre', 'foto_tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_tipo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CentralForm(forms.ModelForm):
    class Meta:
        model = Central
        fields = [
            'nombre', 'foto_central','ubicacion', 'empresa', 'tipo', 'potencia', 'e_media',
            'provincia', 'canton', 'anio_operacion', 'tipo_electrica'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_central': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'potencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'e_media': forms.NumberInput(attrs={'class': 'form-control'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control'}),
            'canton': forms.TextInput(attrs={'class': 'form-control'}),
            'anio_operacion': forms.DateInput(attrs={'class': 'form-control','type': 'number' }),
            'tipo_electrica': forms.Select(attrs={'class': 'form-control'}),
        }

class InformacionCentralForm(forms.ModelForm):
    class Meta:
        model = InformacionCentral
        fields = [
            'capacidad', 'vida_util', 'inversion', 'factor_planta', 'anio', 'central'
        ]
        wigtets = {
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'vida_util': forms.NumberInput(attrs={'class': 'form-control'}),
            'inversion': forms.NumberInput(attrs={'class': 'form-control'}),
            'factor_planta': forms.NumberInput(attrs={'class': 'form-control'}),
            'anio': forms.DateInput(attrs={'class': 'form-control','type': 'date' }),
            'central': forms.Select(attrs={'class': 'form-control'}),
        }
        

class FotovoltaicaForm(forms.ModelForm):
    class Meta:
        model = Fotovoltaica
        fields = '__all__'
        widgets = {
            'central': forms.Select(attrs={'class': 'campo-lcoe'}),
            'anio_ingreso': forms.NumberInput(attrs={'class': 'campo-lcoe'}),
            'numero_paneles': forms.NumberInput(attrs={'class': 'campo-lcoe'}),
            'sistema': forms.TextInput(attrs={'class': 'campo-lcoe'}),
            'potencia_nominal': forms.NumberInput(attrs={'class': 'form-control'}),
            'potencia_efectiva': forms.NumberInput(attrs={'class': 'form-control'}),
            'energia_anual_producida': forms.NumberInput(attrs={'class': 'form-control'}),
            'energia_bruta_calculada': forms.NumberInput(attrs={'class': 'form-control'}),
            'factor_planta': forms.NumberInput(attrs={'class': 'form-control'}),
            'vida_util': forms.NumberInput(attrs={'class': 'form-control'}),
            'degradacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'inversion_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'capital_propio': forms.NumberInput(attrs={'class': 'form-control'}),
            'acreedor': forms.TextInput(attrs={'class': 'form-control'}),
            'deuda': forms.NumberInput(attrs={'class': 'form-control'}),
            'tasa_interes_anual': forms.NumberInput(attrs={'class': 'form-control'}),
            'tasa_interes_periodo': forms.NumberInput(attrs={'class': 'form-control'}),
            'periodos_por_anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'anios_pago_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_periodos': forms.NumberInput(attrs={'class': 'form-control'}),
            'anios_gracia': forms.NumberInput(attrs={'class': 'form-control'}),
            'periodos_gracia': forms.NumberInput(attrs={'class': 'form-control'}),
            'periodos_pago': forms.NumberInput(attrs={'class': 'form-control'}),
            'anios_pago': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_variable': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_produccion': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_anual_oma': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_anual_oma_inversion': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_anual_oma_mw': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # centrales tipo Fotovoltaica
        centrales_fv = Central.objects.filter(tipo_electrica__nombre='Fotovoltaica')
        #  centrales ya usadas en otra instancia de Fotovoltaica
        usadas = Fotovoltaica.objects.values_list('central_id', flat=True)
        # Excluir las que ya están asignadas (excepto si estamos editando y la central ya es la suya)
        if self.instance.pk:
            usadas = usadas.exclude(pk=self.instance.central_id)
        self.fields['central'].queryset = centrales_fv.exclude(id__in=usadas)

