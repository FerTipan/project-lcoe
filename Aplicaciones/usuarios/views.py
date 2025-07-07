from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import CustomLoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Perfil
import random
from django.core.mail import send_mail
from django.conf import settings

@login_required
def custom_logout(request):
    logout(request)
    return redirect('inicio')

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = CustomLoginForm

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)

def registro_view(request):
    # Paso 2: Validar código de verificación
    if request.method == 'POST' and 'codigo_verificacion' in request.POST:
        registro_data = request.session.get('registro_data')
        codigo_enviado = request.session.get('codigo_verificacion')
        codigo_usuario = request.POST.get('codigo_verificacion')

        # Reconstruir el formulario con los datos guardados
        form = RegisterForm(registro_data)
        if codigo_usuario == codigo_enviado:
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                Perfil.objects.get_or_create(user=user)
                # Limpiar sesión
                request.session.pop('registro_data', None)
                request.session.pop('codigo_verificacion', None)
                messages.success(request, "Registro exitoso. Ahora puede iniciar sesión.")
                return redirect('login')
        else:
            messages.error(request, "El código ingresado es incorrecto.")
        # Si el código es incorrecto, vuelve a mostrar solo el campo de código
        return render(request, 'usuarios/registro.html', {
            'form': form,
            'mostrar_campo_codigo': True
        })

    # Paso 1: Recibir datos del formulario y enviar código
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Guardar datos en sesión
            request.session['registro_data'] = request.POST
            # Generar código
            codigo = str(random.randint(100000, 999999))
            request.session['codigo_verificacion'] = codigo
            # Enviar correo
            email = form.cleaned_data['email']
            send_mail(
                'Código de verificación',
                f'Tu código de verificación es: {codigo}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.info(request, "Se ha enviado un código de verificación a tu correo.")
            return render(request, 'usuarios/registro.html', {
                'form': form,
                'mostrar_campo_codigo': True
            })
    else:
        form = RegisterForm()
    return render(request, 'usuarios/registro.html', {'form': form})

LoginRequiredMixin
class RedirectAfterLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.perfil.es_admin:
            return redirect('tipoGeneracion')
        return redirect('tipoGeneracion')

@login_required
def vista_administrador(request):
    if request.user.perfil.es_admin:
        return render(request, 'tipoGeneracion.html')
    else:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('tipoGeneracion')