from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def tipoGeneracion(request):
    return render(request, 'tipoGeneracion.html')
