from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CentralFotovoltaica, CentralTermica, TipoElectrica, Central, InformacionCentral
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
    return render(request, 'tecnologias/tipo_tecno.html', {
        'tipo': tipo,
        'centrales': centrales
})
# Obtener info
def obtener_info_central(request, central_id):
    try:
        central = get_object_or_404(Central, id=central_id)
        tipo = central.tipo_electrica.nombre

        # Mapeo de tipo -> clase hija
        tipo_modelo = {
            "Térmica": CentralTermica,
            "Fotovoltaica": CentralFotovoltaica,
        }

        modelo = tipo_modelo.get(tipo)
        if not modelo:
            return JsonResponse({"error": f"Tipo de central no especificada: {tipo}"}, status=400)

        # obtener instancia específica
        obj = modelo.objects.get(id=central.id)

        # obtener información técnica
        info = InformacionCentral.objects.filter(central=central).order_by('-anio').first()

        if not info:
            return JsonResponse({"error": "No hay información técnica asociada a esta central."}, status=404)

        data = {
            "nombre": central.nombre,
            "ubicacion": central.ubicacion,
            "empresa": central.empresa,
            "potencia": central.potencia,
            "tipo": tipo,
            "informacion": {
                "capacidad": info.capacidad,
                "vida_util": info.vida_util,
                "inversion": info.inversion,
                "factor_planta": info.factor_planta,
                "anio": info.anio,
            },
        }
        # Agregar detalles específicos de cada tipo
        if hasattr(obj, 'to_dict'):
            data["detalles_tipo"] = obj.to_dict()
        else:
            data["detalles_tipo"] = {}

        return JsonResponse(data)

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# Tecnologias
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