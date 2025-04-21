from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from biblioteca import views_admin 


urlpatterns = [
    path('', lambda request: redirect('index')), 
    path('usuario/', include('biblioteca.urls_usuario')),
    path('adminpanel/', include('biblioteca.urls_admin')),
    path('admin/', admin.site.urls),  
]