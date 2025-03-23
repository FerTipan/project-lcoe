from django.shortcuts import render
def inicio (request): #funcion para presentar en pantalla el codigo html del template inicio.html
    return render(request,'inicio.html')

# Create your views here.
