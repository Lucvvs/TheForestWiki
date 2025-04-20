from django.urls import path
from django.shortcuts import redirect
from .views import index, registro, foro, inicio_sesion, mi_cuenta, compra, pagar, carrito # Importa las vistas directamente desde views

urlpatterns = [
    path('', lambda request: redirect('index/')),
    path('index/', index, name='index'),
    path('index/registro.html', registro, name='registro'),
    path('index/foro.html', foro, name='foro'),
    path('index/inicio_sesion.html', inicio_sesion, name='inicio_sesion'),
    path('index/mi_cuenta.html', mi_cuenta, name='mi_cuenta'),
    path('index/compra.html', compra, name='compra'),
    path('index/pagar.html', pagar, name='pagar'),
    path('index/carrito.html', pagar, name='carrito'),

]
