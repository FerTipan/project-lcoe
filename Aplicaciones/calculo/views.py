from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import  TipoElectrica, Central, InformacionCentral, Fotovoltaica, Termica, Eolica, Hidraulica, CasoCalculo, ResultadoCalculo , ParametroFotovoltaica, ParametroEolica, ParametroHidraulica
from .forms import TipoElectricaForm, CentralForm, InformacionCentralForm, FotovoltaicaForm, TermicaForm, EolicaForm, HidraulicaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from .services import crear_parametros_desde_tipo_generacion
from django.contrib.auth.decorators import login_required
# Importacion de la app usuarios
from Aplicaciones.usuarios.models import Perfil
from django.views.generic import TemplateView
from Aplicaciones.usuarios.decorators import AdminRequiredMixin, UserRequiredMixin
from django.urls import reverse

@login_required
def vista_usuario_calculo(request):
    return render(request, 'calculo/tipoGeneracion.html')

def inicio(request):
    return render(request, 'inicio.html')

@login_required
def tipoGeneracion(request):
    tipos = TipoElectrica.objects.all()
    return render(request, 'tipoGeneracion.html', {'tipos': tipos})

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'calculo/tipoGeneracion.html'

class UserDashboardView(UserRequiredMixin, TemplateView):
    template_name = 'calculo/tipoGeneracion.html'

# ------------------------------- TIPO ELECTRICA -----------------------------------
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

# ------------------------------- CENTRAL -----------------------------------
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

# ------------------------------- FOTOVOLTAICA -----------------------------------
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
    

# ------------------------------- TERMICA -----------------------------------
class TermicaListView(ListView):
    model = Termica
    template_name = 'termica/listaT.html'

    def get_queryset(self):
        return Termica.objects.filter(central__tipo_electrica__nombre__icontains='termica')

class TermicaCreateView(CreateView):
    model = Termica
    form_class = TermicaForm
    template_name = 'termica/formT.html'
    success_url = reverse_lazy('termica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central termica agregada correctamente.')
        return super().form_valid(form)
    
class TermicaUpdateView(UpdateView):
    model = Termica
    form_class = TermicaForm
    template_name = 'termica/formT.html'
    success_url = reverse_lazy('termica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central termica actualizada correctamente.')
        return super().form_valid(form)

class TermicaDeleteView(DeleteView):
    model = Termica
    success_url = reverse_lazy('termica_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Central fotovoltaica eliminada correctamente.')
        return super().delete(request, *args, **kwargs)

# ------------------------------- EOLICA -----------------------------------
class EolicaListView(ListView):
    model = Eolica
    template_name = 'eolica/listaE.html'

    def get_queryset(self):
        return Eolica.objects.filter(central__tipo_electrica__nombre__icontains='eolica')
    
class EolicaCreateView(CreateView):
    model = Eolica
    form_class = EolicaForm
    template_name = 'eolica/formE.html'
    success_url = reverse_lazy('eolica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central eolica agregada correctamente.')
        return super().form_valid(form)
    

class EolicaUpdateView(UpdateView):
    model = Eolica
    form_class = EolicaForm
    template_name = 'eolica/formE.html'
    success_url = reverse_lazy('eolica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central eolica actualizada correctamente.')
        return super().form_valid(form)

class EolicaDeleteView(DeleteView):
    model = Eolica
    success_url = reverse_lazy('eolica_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Central eolica eliminada correctamente.')
        return super().delete(request, *args, **kwargs)
 
# ------------------------------- HIDRAULICA -----------------------------------
class HidraulicaListView(ListView):
    model = Hidraulica
    template_name = 'hidraulica/listaH.html'

    def get_queryset(self):
        return Hidraulica.objects.filter(central__tipo_electrica__nombre__icontains='hidraulica')
    
class HidraulicaCreateView(CreateView):
    model = Hidraulica
    form_class = HidraulicaForm  
    template_name = 'hidraulica/formH.html'
    success_url = reverse_lazy('hidraulica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central hidraulica agregada correctamente.')
        return super().form_valid(form)
    
class HidraulicaUpdateView(UpdateView):
    model = Hidraulica
    form_class = HidraulicaForm  
    template_name = 'hidraulica/formH.html'
    success_url = reverse_lazy('hidraulica_list')

    def form_valid(self, form):
        messages.success(self.request, 'Central hidroeléctrica actualizada correctamente.')
        return super().form_valid(form)
    
class HidraulicaDeleteView(DeleteView):
    model = Hidraulica
    success_url = reverse_lazy('hidraulica_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Central hidroeléctrica eliminada correctamente.')
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

def mapa(request):
    lugares = [
        {"nombre": "Lugar 1", "lat": -1.8312, "lng": -78.1834},
        {"nombre": "Lugar 2", "lat": -0.1807, "lng": -78.4747},
    ]
    return render(request, 'mapa.html', {'lugares': lugares})

def mapa_detalle(request, pagina):
    return render(request, f'tecnologias/{pagina}.html')

# ------------------------------- CENTRALES POR TIPO -----------------------------------
@login_required
def centrales_por_tipo(request, tipo_id):
    tipo = get_object_or_404(TipoElectrica, id=tipo_id)
    centrales = Central.objects.filter(tipo_electrica=tipo)

    centrales_con_tipo = []
    for central in centrales:
        if hasattr(central, 'fotovoltaica'):
            tipo_especifico = 'fotovoltaica'
        elif hasattr(central, 'termica'):
            tipo_especifico = 'termica'
        elif hasattr(central, 'eolica'):
            tipo_especifico = 'eolica'
        elif hasattr(central, 'hidraulica'):
            tipo_especifico = 'hidraulica'
        else:
            tipo_especifico = 'general'

        centrales_con_tipo.append({
            'id': central.id,
            'nombre': central.nombre,
            'tipo_especifico': tipo_especifico,
            'potencia': central.potencia,
            'ubicacion': central.provincia,
        })

    central_seleccionada = None
    resultado = None
    caso = None

    try:
        perfil_usuario = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        messages.error(request, "No tienes un perfil asociado.")
        return redirect('inicio')

    if request.method == "POST":
        central_id = request.POST.get("central_id")
        central_seleccionada = get_object_or_404(Central, id=central_id)

        # Crear el caso de cálculo
        caso = CasoCalculo.objects.create(
            nombre=f"Cálculo de {central_seleccionada.nombre}",
            usuario=perfil_usuario,
            central=central_seleccionada
        )

        parametros = crear_parametros_desde_tipo_generacion(caso)

        if not parametros:
            messages.error(request, "No se pudo crear los parámetros para esta tecnología.")
            return redirect('centrales_por_tipo', tipo_id=tipo_id)
        else:
            try:
                lcoe_valor = parametros.calcular_lcoe()
                if isinstance(lcoe_valor, dict) and 'error' in lcoe_valor:
                    messages.error(request, f"No se pudo calcular el LCOE: {lcoe_valor['error']}")
                else:
                    resultado = ResultadoCalculo.objects.create(
                        caso=caso,
                        lcoe=lcoe_valor,
                    )
                    messages.success(request, "Cálculo realizado exitosamente.")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al calcular o guardar el resultado: {e}")
            return redirect(f"{reverse('centrales_por_tipo', args=[tipo_id])}?caso_id={caso.id}")

    # --- GET ---
    caso_id = request.GET.get("caso_id")
    if caso_id:
        try:
            caso = CasoCalculo.objects.get(pk=caso_id)
            central_seleccionada = caso.central
            resultado = ResultadoCalculo.objects.filter(caso=caso).last()
        except CasoCalculo.DoesNotExist:
            caso = None
            central_seleccionada = None
            resultado = None

    return render(request, 'tecnologias/seleccion.html', {
        'tipo': tipo,
        'centrales': centrales_con_tipo,
        'central_seleccionada': central_seleccionada,
        'resultado': resultado,
        'caso': caso,
    })
# ---------------------  Nuevo caso CALCULOS LCOE --------------------  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import io
import base64

@login_required
@csrf_exempt
def nuevo_caso_calculo(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            central_id = request.POST.get('central_id')
            comparar_con_id = request.POST.get('comparar_con_id')
            central = Central.objects.get(id=central_id) if central_id else None

            caso = CasoCalculo.objects.create(
                nombre=nombre,
                usuario=request.user.perfil,
                central=central,
                es_simulacion=True
            )

            parametros = ParametroFotovoltaica.objects.create(
                caso=caso,
                potencia_nominal=request.POST.get('potencia_nominal'),
                factor_planta=request.POST.get('factor_planta'),
                vida_util=request.POST.get('vida_util'),
                inversion_total=request.POST.get('inversion_total'),
                porcentaje_capital_propio=request.POST.get('porcentaje_capital_propio'),
                porcentaje_deuda=request.POST.get('porcentaje_deuda'),
                capital_propio=request.POST.get('capital_propio'),
                deuda=request.POST.get('deuda'),
                costo_variable=request.POST.get('costo_variable'),
                costo_produccion=request.POST.get('costo_produccion'),
                costo_anual_oma_mw=request.POST.get('costo_anual_oma_mw'),
                energia_anual_producida=request.POST.get('energia_anual_producida'),
                tasa_interes_periodo=request.POST.get('tasa_interes_periodo'),
                tasa_interes_anual=request.POST.get('tasa_interes_anual'),
                total_periodos=request.POST.get('total_periodos'),
                anios_gracia=request.POST.get('anios_gracia'),
                periodos_pago=request.POST.get('periodos_pago'),
                beta=request.POST.get('beta'),
                margen_intermediacion=request.POST.get('margen_intermediacion'),
                inflacion=request.POST.get('inflacion'),
                economia=request.POST.get('economia'),
                riesgo=request.POST.get('riesgo'),
                sin_riesgo=request.POST.get('sin_riesgo'),
                tasa_mercado=request.POST.get('tasa_mercado'),
                premio_riesgo_mercado=request.POST.get('premio_riesgo_mercado'),
                impuesto=request.POST.get('impuesto'),
                degradacion=request.POST.get('degradacion'),
                tasa_descuento=Decimal(request.POST["tasa_descuento"]),
            )

            resultado = ResultadoCalculo.objects.create(caso=caso)

            if resultado.lcoe is None:
                return JsonResponse({
                    "status": "error",
                    "message": "No se pudo calcular el LCOE. Verifique los datos ingresados."
                })

            # Comparar con otra tecnología existente si se proporcionó
            lcoe_base = float(resultado.lcoe)
            nombres = ["Nuevo Caso"]
            valores = [lcoe_base]

            if comparar_con_id:
                central_comp = Central.objects.get(id=comparar_con_id)
                caso_existente = CasoCalculo.objects.filter(central=central_comp).last()
                if caso_existente and hasattr(caso_existente, 'resultadocalculo') and caso_existente.resultadocalculo.lcoe:
                    nombres.append(central_comp.nombre)
                    valores.append(float(caso_existente.resultadocalculo.lcoe))

            # Generar gráfica con matplotlib
            fig, ax = plt.subplots()
            ax.bar(nombres, valores, color=["#4CAF50", "#FF9800"])
            ax.set_ylabel("LCOE (USD/kWh)")
            ax.set_title("Comparación de LCOE")

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()

            return JsonResponse({
                "status": "ok",
                "lcoe": lcoe_base,
                "nombre": caso.nombre,
                "id": caso.id,
                "grafico": image_base64
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Método no permitido"})
