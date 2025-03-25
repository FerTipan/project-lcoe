from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def tipoGeneracion(request):
    return render(request, 'tipoGeneracion.html')

def eolica(request):
    return render(request, 'tecnologias/eolica.html')

def solar(request):
    return render(request, 'tecnologias/solar.html')

def hidraulica(request):
    return render(request, 'tecnologias/hidraulica.html')

def termica(request):
    return render(request, 'tecnologias/termica.html')
