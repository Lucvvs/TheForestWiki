from django.urls import path
from . import views_admin as views

urlpatterns = [
    path('publicaciones/', views.AdminPublicacionList.as_view(), name='admin_publicaciones'),
    path('publicaciones/nueva/', views.AdminPublicacionCreate.as_view(), name='admin_pub_nueva'),
    path('usuarios/', views.AdminUsuarioList.as_view(), name='admin_usuarios'),
]