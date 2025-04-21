from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User  # ✅ Usamos el modelo de Django
from .models import Publicacion


# 🔒 Mixin: Solo admins
class SoloAdmins(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('inicio_sesion')


# 👤 Gestión de usuarios
class AdminUsuarioList(SoloAdmins, ListView):
    model = User  # ✅ Cambiado a User de Django
    template_name = 'admin/usuarios_admin.html'
    context_object_name = 'usuarios'


# 📝 Gestión de publicaciones
class AdminPublicacionList(SoloAdmins, ListView):
    model = Publicacion
    template_name = 'admin/publicaciones_admin.html'
    context_object_name = 'publicaciones'


class AdminPublicacionCreate(SoloAdmins, CreateView):
    model = Publicacion
    fields = ['titulo', 'contenido', 'categoria']
    template_name = 'admin/publicacion_form.html'
    success_url = reverse_lazy('admin_publicaciones')