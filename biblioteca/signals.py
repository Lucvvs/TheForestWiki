from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria
from django.db import connection

@receiver(post_migrate)
def cargar_categorias_iniciales(sender, **kwargs):
    if sender.name != 'biblioteca':
        return

    if 'biblioteca_categoria' in connection.introspection.table_names():
        categorias_defecto = [
            "Animales", "Mapa", "Enemigos", "Construcciones",
            "Plantas", "Comunidad", "Bugs", "Objetos"
        ]
        for nombre in categorias_defecto:
            Categoria.objects.get_or_create(nombre_categoria=nombre)
    else:
        print("⚠️ Tabla Categoria no está disponible todavía")