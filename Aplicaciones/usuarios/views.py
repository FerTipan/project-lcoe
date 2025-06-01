from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def login_view(request):
    return render(request, 'usuarios/login.html')

@login_required
def redireccion_por_rol(request):
    if request.user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')  # vista - admin
    else:
        return redirect('tipoGeneracion')  # vista - usuario
    
@login_required
def dashboard_admin(request):
    return render(request, 'usuarios/dashboard_admin.html')


def custom_logout(request):
    logout(request)
    return redirect('inicio')


#from .forms import PerfilForm

''' @login_required
def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("tipoTecno")
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'usuarios/editar_perfil.html', {'form': form}) '''