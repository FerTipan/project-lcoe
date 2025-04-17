from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CentralTermica, TipoElectrica, Central, InformacionCentral
from .forms import TipoElectricaForm, CentralForm, InformacionCentralForm

# TipoElectrica
class TipoElectricaListView(ListView):
    model = TipoElectrica

class TipoElectricaCreateView(CreateView):
    model = TipoElectrica
    form_class = TipoElectricaForm
    success_url = reverse_lazy('tipoelectrica_list')

class TipoElectricaUpdateView(UpdateView):
    model = TipoElectrica
    form_class = TipoElectricaForm
    success_url = reverse_lazy('tipoelectrica_list')

class TipoElectricaDeleteView(DeleteView):
    model = TipoElectrica
    success_url = reverse_lazy('tipoelectrica_list')

# Central
class CentralListView(ListView):
    model = Central

class CentralCreateView(CreateView):
    model = Central
    form_class = CentralForm
    success_url = reverse_lazy('central_list')

class CentralUpdateView(UpdateView):
    model = Central
    form_class = CentralForm
    success_url = reverse_lazy('central_list')

class CentralDeleteView(DeleteView):
    model = Central
    success_url = reverse_lazy('central_list')

# InformacionCentral
class InformacionCentralListView(ListView):
    model = InformacionCentral

class InformacionCentralCreateView(CreateView):
    model = InformacionCentral
    form_class = InformacionCentralForm
    success_url = reverse_lazy('info_list')

class InformacionCentralUpdateView(UpdateView):
    model = InformacionCentral
    form_class = InformacionCentralForm
    success_url = reverse_lazy('info_list')

class InformacionCentralDeleteView(DeleteView):
    model = InformacionCentral
    success_url = reverse_lazy('info_list')

# Views
def inicio(request):
    return render(request, 'inicio.html')

def tipoGeneracion(request):
    tipos = TipoElectrica.objects.all()
    return render(request, 'tipoGeneracion.html', {'tipos': tipos})


#Centrales por tipo
def centrales_por_tipo(request, tipo_id):
    tipo = get_object_or_404(TipoElectrica, id=tipo_id)
    centrales = Central.objects.filter(tipo_electrica=tipo)
    return render(request, 'tecnologias/termica.html', {
        'tipo': tipo,
        'centrales': centrales
})
# Obtener info
def obtener_info_central(request, central_id):
    try:
        central = Central.objects.get(id=central_id)
        tipo = central.tipo.nombre

        # Luego según tipo de generación
        if tipo == 'Térmica':
            obj = CentralTermica.objects.get(id=central.id)
            data = {
                "tipo": tipo,
                "capacidad": obj.capacidad,
                "vida_util": obj.vida_util,
                "anio": obj.anio,
                "inversion_total": obj.inversion_total,
                "factor_planta": obj.factor_planta,
                "costos_produccion": obj.costos_produccion,
                "costos_om": obj.costos_om,
                "costos_variable": obj.costos_variable,
            }
        elif tipo == 'Hidráulica':
            obj = CentralTermica.objects.get(id=central.id)
            data = {
                "tipo": tipo,
                "capacidad": obj.capacidad,
                "vida_util": obj.vida_util,
                "anio": obj.anio,
                "altura_neta": obj.altura_neta,
                "caudal_diseno": obj.caudal_diseno,
                "eficiencia": obj.eficiencia,
            }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def eolica(request):
    return render(request, 'tecnologias/eolica.html')

def solar(request):
    return render(request, 'tecnologias/solar.html')

def hidraulica(request):
    return render(request, 'tecnologias/hidraulica.html')

def termica(request):
    return render(request, 'tecnologias/termica.html')

def login(request):
    return render(request, 'login.html')

def informacion(request):

    return render(request, 'tecnologias/termica.html')