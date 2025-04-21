from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria

@receiver(post_migrate)
def crear_categorias_por_defecto(sender, **kwargs):
    categorias_defecto = [
        "Animales", "Mapa", "Enemigos", "Construcciones",
        "Plantas", "Comunidad", "Bugs", "Objetos"
    ]
    for nombre in categorias_defecto:
        Categoria.objects.get_or_create(nombre_categoria=nombre)