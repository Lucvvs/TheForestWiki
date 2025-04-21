from django.contrib import admin
from .models import (
    Usuario,
    TipoUsuario,
    Publicacion,
    Comentario,
    Juego,
    Categoria,
    TipoReaccion,
    VersionJuego
)

admin.site.register(Usuario)
admin.site.register(TipoUsuario)
admin.site.register(Publicacion)
admin.site.register(Comentario)
admin.site.register(Juego)
admin.site.register(Categoria)
admin.site.register(TipoReaccion)
admin.site.register(VersionJuego)