from django.shortcuts import render, redirect
from django.contrib import messages 

def index(request):
    return render(request, 'index.html')

def registro(request):
    if request.method == 'POST':
        # Aquí iría la lógica de registro real, pero por ahora solo mostramos el mensaje
        messages.success(request, '¡Registro exitoso! Disfruta la experiencia.')
        return redirect('registro')  # Redirige para evitar el reenvío del formulario
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