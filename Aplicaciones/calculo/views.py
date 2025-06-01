from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import  TipoElectrica, Central, InformacionCentral, Fotovoltaica, CasoCalculo, ResultadoCalculo 
from .forms import TipoElectricaForm, CentralForm, InformacionCentralForm, FotovoltaicaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
import json
from .services import crear_parametros_desde_fotovoltaica
from django.contrib.auth.decorators import login_required
# Importacion de la app usuarios
from Aplicaciones.usuarios.models import Perfil


@login_required
def vista_usuario_calculo(request):
    return render(request, 'calculo/tipoGeneracion.html')

# TipoElectrica
class TipoElectricaListView(ListView):
    model = TipoElectrica

class TipoElectricaCreateView(CreateView):
    model = TipoElectrica
    form_class = TipoElectricaForm
    success_url = reverse_lazy('tipoelectrica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de Generación creada correctamente')
        return super().form_valid(form)

class TipoElectricaUpdateView(UpdateView):
    model = TipoElectrica
    form_class = TipoElectricaForm
    success_url = reverse_lazy('tipoelectrica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Datos actualizados correctamente')
        return super().form_valid(form)

class TipoElectricaDeleteView(DeleteView):
    model = TipoElectrica
    success_url = reverse_lazy('tipoelectrica_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tipo de Generación eliminado correctamente')
        return super().delete(request, *args, **kwargs)

# Central
class CentralListView(ListView):
    model = Central

class CentralCreateView(CreateView):
    model = Central
    form_class = CentralForm
    success_url = reverse_lazy('central_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central creada correctamente')
        return super().form_valid(form)
    
class CentralUpdateView(UpdateView):
    model = Central
    form_class = CentralForm
    success_url = reverse_lazy('central_list')

    def form_valid(self, form):
        messages.success(self.request, 'Datos de la Central actualizados correctamente')
        return super().form_valid(form)

class CentralDeleteView(DeleteView):
    model = Central
    success_url = reverse_lazy('central_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Central eliminada correctamente')
        return super().delete(request, *args, **kwargs)
    
class FotovoltaicaListView(ListView):
    model = Fotovoltaica
    template_name = 'fotovoltaica/lista.html'

    def get_queryset(self):
        return Fotovoltaica.objects.filter(central__tipo_electrica__nombre__icontains='fotovoltaica')

class FotovoltaicaCreateView(CreateView):
    model = Fotovoltaica
    form_class = FotovoltaicaForm
    template_name = 'fotovoltaica/form.html'
    success_url = reverse_lazy('fotovoltaica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central fotovoltaica agregada correctamente.')
        return super().form_valid(form)
    

class FotovoltaicaUpdateView(UpdateView):
    model = Fotovoltaica
    form_class = FotovoltaicaForm
    template_name = 'fotovoltaica/form.html'
    success_url = reverse_lazy('fotovoltaica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central fotovoltaica actualizada correctamente.')
        return super().form_valid(form)

class FotovoltaicaDeleteView(DeleteView):
    model = Fotovoltaica
    success_url = reverse_lazy('fotovoltaica_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Central fotovoltaica eliminada correctamente.')
        return super().delete(request, *args, **kwargs)
    
# InformacionCentral
class InformacionCentralListView(ListView):
    model = InformacionCentral

class InformacionCentralCreateView(CreateView):
    model = InformacionCentral
    form_class = InformacionCentralForm
    success_url = reverse_lazy('info_list')

    def form_valid(self, form):
        messages.success(self.request, 'Datos ingresados correctamente')
        return super().form_valid(form)

class InformacionCentralUpdateView(UpdateView):
    model = InformacionCentral
    form_class = InformacionCentralForm
    success_url = reverse_lazy('info_list')

    def form_valid(self, form):
        messages.success(self.request, 'Datos actualizados correctamente')
        return super().form_valid(form)

class InformacionCentralDeleteView(DeleteView):
    model = InformacionCentral
    success_url = reverse_lazy('info_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Datos eliminados correctamente')
        return super().delete(request, *args, **kwargs)

def inicio(request):
    return render(request, 'inicio.html')

def tipoGeneracion(request):
    tipos = TipoElectrica.objects.all()
    return render(request, 'tipoGeneracion.html', {'tipos': tipos})

def mapa(request):
    lugares = [
        {"nombre": "Lugar 1", "lat": -1.8312, "lng": -78.1834},
        {"nombre": "Lugar 2", "lat": -0.1807, "lng": -78.4747},
    ]
    return render(request, 'mapa.html', {'lugares': lugares})

def mapa_detalle(request, pagina):
    # Asegúrate de que la variable 'pagina' no tenga la extensión .html
    return render(request, f'tecnologias/{pagina}.html')

# ------------- Centrales por tipo --------------
@login_required
def centrales_por_tipo(request, tipo_id):
    tipo = get_object_or_404(TipoElectrica, id=tipo_id)
    centrales = Central.objects.filter(tipo_electrica=tipo)

    centrales_con_tipo = []
    for central in centrales:
        if hasattr(central, 'fotovoltaica'):
            tipo_especifico = 'fotovoltaica'
        else:
            tipo_especifico = 'general'

        centrales_con_tipo.append({
            'id': central.id,
            'nombre': central.nombre,
            'tipo_especifico': tipo_especifico,
            'potencia': central.potencia,
            'ubicacion': f"{central.provincia}, {central.canton}"
        })

    central_seleccionada = None
    resultado = None
    caso = None

    try:
        perfil_usuario = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        messages.error(request, "No tienes un perfil asociado.")
        #return redirect('seleccion', tipo_id=tipo.id)

    if request.method == "POST":
        central_id = request.POST.get("central_id")
        central_seleccionada = get_object_or_404(Central, id=central_id)

        caso = CasoCalculo.objects.create(
            nombre=f"Cálculo de {central_seleccionada.nombre}",
            usuario=perfil_usuario,
            central=central_seleccionada
        )

        crear_parametros_desde_fotovoltaica(caso)
        resultado = ResultadoCalculo.objects.create(caso=caso)
        resultado.save()

    return render(request, 'tecnologias/seleccion.html', {
        'tipo': tipo,
        'centrales': centrales_con_tipo,
        'central_seleccionada': central_seleccionada,
        'resultado': resultado,
        'caso': caso
    })

# ----------- VISUALIZACION DE INFO -------------
@login_required
def calculo_view(request):
    centrales = Central.objects.all()
    central_seleccionada = None
    resultado = None
    caso = None

    if request.method == "POST":
        central_id = request.POST.get("central_id")
        central_seleccionada = Central.objects.get(id=central_id)
        
        caso = CasoCalculo.objects.create(
            nombre=f"Cálculo de {central_seleccionada.nombre}",
            #usuario=request.user.perfil,
            central=central_seleccionada
        )
        crear_parametros_desde_fotovoltaica(caso)
        resultado = ResultadoCalculo.objects.create(caso=caso)
        resultado.save()

    return render(request, '/calculo_lcoe.html', {
        'centrales': centrales,
        'central_seleccionada': central_seleccionada,
        'caso': caso,
        'resultado': resultado
    })


# ---------------------  CALCULOS LCOE --------------------  
@login_required
def crear_caso_y_calcular(request, central_id):
    central = Central.objects.get(id=central_id)

    caso = CasoCalculo.objects.create(
        nombre=f"Cálculo de {central.nombre}",
        usuario=request.user.perfil,
        central=central
    )

    crear_parametros_desde_fotovoltaica(caso)

    resultado = ResultadoCalculo.objects.create(caso=caso)
    resultado.save()  

    return redirect('ver_resultado', caso_id=caso.id)


def ver_resultado(request, caso_id):
    caso = CasoCalculo.objects.get(id=caso_id)
    resultado = caso.resultadocalculo
    return render(request, 'resultados/result.html', {'caso': caso, 'resultado': resultado})
