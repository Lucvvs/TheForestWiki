from django.urls import path
from . import views  # Asegúrate de importar tus vistas

urlpatterns = [
    path('', views.home, name='home'),
]
