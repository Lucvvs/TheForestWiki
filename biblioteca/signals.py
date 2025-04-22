from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Publicacion, Categoria
from django.db import connection
from django.contrib.auth.models import User

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



@receiver(post_migrate)
def crear_publicaciones_default(sender, **kwargs):
    if sender.name != 'biblioteca':
        return

    usuario = User.objects.filter(is_superuser=True).first()
    if not usuario:
        usuario = User.objects.create_user(
            username='admin', password='admin1234', email='admin@forestwiki.com'
        )
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save()

    categorias = {
        "Mapa": Categoria.objects.get_or_create(nombre_categoria="Mapa")[0],
        "Enemigos": Categoria.objects.get_or_create(nombre_categoria="Enemigos")[0],
        "Construcciones": Categoria.objects.get_or_create(nombre_categoria="Construcciones")[0],
        "Plantas": Categoria.objects.get_or_create(nombre_categoria="Plantas")[0],
        "Objetos": Categoria.objects.get_or_create(nombre_categoria="Objetos")[0],
    }

    publicaciones = [
        ("Zonas importantes del mapa", "Explora las zonas clave y puntos de interés del mapa.", "Mapa"),
        ("Los enemigos más peligrosos", "Te contamos cuáles son los enemigos que debes evitar a toda costa.", "Enemigos"),
        ("Cómo construir una base segura", "Guía para armar una base impenetrable.", "Construcciones"),
        ("Plantas comestibles vs venenosas", "Aprende a diferenciar entre plantas que curan y las que matan.", "Plantas"),
        ("Lista de objetos esenciales", "Objetos que no pueden faltar en tu mochila.", "Objetos"),
    ]

    for titulo, contenido, nombre_cat in publicaciones:
        Publicacion.objects.get_or_create(
            titulo=titulo,
            defaults={
                'contenido': contenido,
                'usuario': usuario,
                'categoria': categorias[nombre_cat],
            }
        )



def crear_superusuario_default(sender, **kwargs):
    if sender.name != 'biblioteca':
        return

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@forestwiki.com',
            password='admin1234'
        )
        print("✅ Superusuario 'admin' creado por defecto.")
    else:
        print("ℹ️ El superusuario 'admin' ya existe.")

        
