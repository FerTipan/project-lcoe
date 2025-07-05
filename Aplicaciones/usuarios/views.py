from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import CustomLoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Perfil

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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            Perfil.objects.get_or_create(user=user)

            messages.success(request, "Registro exitoso. Ahora puede iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Por favor llena los campos.")
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