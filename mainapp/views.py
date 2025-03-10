from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"index.html")

def terminos(request):
    return render(request,"terminos.html")

def privacidad(request):
    return render(request, "privacidad.html")

def is_masculino(x):
    if x=="m":
        return "Genero: Masculino"
    else:
        return "Genero: Femenino"
