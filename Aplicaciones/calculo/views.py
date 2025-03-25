from django.shortcuts import render
def inicio (request): #funcion para presentar en pantalla el codigo html del template inicio.html
    return render(request,'inicio.html')

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def tipoGeneracion(request):
    return render(request, 'tipoGeneracion.html')
