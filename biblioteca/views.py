from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def registro(request):
    return render(request, 'registro.html')

def foro(request):
    return render(request, 'foro.html')

def inicio_sesion(request):
    return render(request, 'inicio_sesion.html')

def mi_cuenta(request):
    return render(request, 'mi_cuenta.html')

def compra(request):
    return render(request, 'compra.html')

def pagar(request):
    return render(request, 'pagar.html')

def carrito(request):
    return render(request, 'carrito.html')