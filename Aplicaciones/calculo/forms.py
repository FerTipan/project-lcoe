from django import forms
from .models import ResultadoCalculo, TipoElectrica, Central, InformacionCentral, Fotovoltaica
from .models import CasoCalculo, ParametroCalculos

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
            'nombre', 'foto_central','ubicacion', 'empresa', 'tipo', 'potencia',
            'provincia', 'anio_operacion', 'tipo_electrica'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_central': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'potencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control'}),
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
            'central': forms.Select(attrs={'class': 'form-control campo-lcoe'}),
            'anio_ingreso': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'numero_paneles': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'sistema': forms.TextInput(attrs={'class': 'form-control campo-lcoe'}),
            'potencia_nominal': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'potencia_efectiva': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'factor_planta': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'vida_util': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'degradacion': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'inversion_total': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'porcentaje_capital_propio': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'porcentaje_deuda': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'acreedor': forms.TextInput(attrs={'class': 'form-control campo-lcoe'}),
            'tasa_interes_periodo': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'periodos_por_anio': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'anios_pago_total': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'anios_gracia': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'costo_variable': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'beta': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'margen_intermediacion': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'inflacion': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'economia': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'riesgo': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'sin_riesgo': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'tasa_mercado': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'premio_riesgo_mercado': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'impuesto': forms.NumberInput(attrs={'class': 'form-control campo-lcoe'}),
            'costo_produccion': forms.NumberInput(attrs={'class': 'form-control campo-lcoe '}),


            # Campos calculados (pueden ser mostrados como solo lectura)
            'energia_anual_producida': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'energia_bruta_calculada': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'capital_propio': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'deuda': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'tasa_interes_anual': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'total_periodos': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'periodos_gracia': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'periodos_pago': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'anios_pago': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'costo_anual_oma': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'costo_anual_oma_inversion': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'costo_anual_oma_mw': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
            'indice_premio': forms.NumberInput(attrs={'class': 'form-control campo-lcoe bg-light', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(FotovoltaicaForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control campo-lcoe'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Centrales cuyo tipo_electrica sea "fotovoltaica", sin importar mayúsculas/minúsculas
        centrales_fv = Central.objects.filter(tipo_electrica__nombre__iexact='FOTOVOLTAICA')
        
        # IDs de centrales ya usadas en otros objetos Fotovoltaica
        usadas = list(Fotovoltaica.objects.values_list('central_id', flat=True))

        # Si estamos editando una instancia existente y su central está en 'usadas', la quitamos para permitir que aparezca
        if self.instance.pk and self.instance.central_id in usadas:
            usadas.remove(self.instance.central_id)

        # Asignamos queryset excluyendo las centrales usadas (excepto la actual si estamos editando)
        self.fields['central'].queryset = centrales_fv.exclude(id__in=usadas)


class CasoYParametrosForm(forms.ModelForm):
    # Incluimos campos del modelo relacionado (ParametroCalculo)
    inversion_total = forms.FloatField()
    energia_anual_producida = forms.FloatField()
    vida_util = forms.FloatField()
    tasa_descuento = forms.FloatField()
    tasa_crecimiento_energia = forms.FloatField(required=False, initial=0.0)
    costo_operacion_anual = forms.FloatField()

    class Meta:
        model = CasoCalculo
        fields = ['nombre', 'central', 'es_simulacion', 'descripcion']

    def save(self, usuario, commit=True):
        caso = super().save(commit=False)
        caso.usuario = usuario
        if commit:
            caso.save()

            # Crear parámetros ligados al caso
            ParametroCalculos.objects.create(
                caso=caso,
                inversion_total=self.cleaned_data['inversion_total'],
                energia_anual_producida=self.cleaned_data['energia_anual_producida'],
                vida_util=self.cleaned_data['vida_util'],
                tasa_descuento=self.cleaned_data['tasa_descuento'],
                tasa_crecimiento_energia=self.cleaned_data.get('tasa_crecimiento_energia', 0.0),
                costo_operacion_anual=self.cleaned_data['costo_operacion_anual'],
            )

            # Crear resultado automáticamente
            ResultadoCalculo.objects.create(caso=caso)

        return caso
