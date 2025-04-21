from django.contrib import admin
from .models import (
    Publicacion,
    Comentario,
    Juego,
    Categoria,
    TipoReaccion,
    Reaccion, 
    VersionJuego

)

admin.site.register(Publicacion)
admin.site.register(Comentario)
admin.site.register(Juego)
admin.site.register(Categoria)
admin.site.register(TipoReaccion)
admin.site.register(Reaccion) 
admin.site.register(VersionJuego)