from django.urls import path
from . import views_usuario as views
from biblioteca import views_usuario  # 👈


urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('foro/', views.foro, name='foro'),
    path('login/', views.inicio_sesion, name='inicio_sesion'),
    path('cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('compra/', views.compra, name='compra'),
    path('pagar/', views.pagar, name='pagar'),
    path('carrito/', views.carrito, name='carrito'),
path('publicacion/<int:id>/', views.publicacion_detalle, name='publicacion_detalle'),
path('logout/', views.cerrar_sesion, name='logout'),

]