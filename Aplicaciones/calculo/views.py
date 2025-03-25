from django.shortcuts import render
def inicio (request): #funcion para presentar en pantalla el codigo html del template inicio.html
    return render(request,'inicio.html')

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def tipoGeneracion(request):
    return render(request, 'tipoGeneracion.html')

def tipoGeneracion(request):
    return render(request, 'tipoGeneracion.html')

def hidraulica(request):
    return render(request, 'tecnologias/hidraulica.html')

def termica(request):
    return render(request, 'tecnologias/termica.html')

def solar(request):
    return render(request, 'tecnologias/solar.html')

def eolica(request):
    return render(request, 'tecnologias/eolica.html')