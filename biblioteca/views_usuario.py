from django.shortcuts import render, get_object_or_404, redirect
from .models import Publicacion, Comentario, Reaccion, TipoReaccion, Usuario
from django.db.models import Count



def foro(request):
    categoria_filtro = request.GET.get('categoria')  # Captura el filtro desde la URL

    if categoria_filtro and categoria_filtro.lower() != 'todo':
        publicaciones = Publicacion.objects.select_related('usuario', 'categoria').filter(
            categoria__nombre_categoria__iexact=categoria_filtro
        ).order_by('-fecha_creacion')
    else:
        publicaciones = Publicacion.objects.select_related('usuario', 'categoria').order_by('-fecha_creacion')

    return render(request, 'foro.html', {
        'publicaciones': publicaciones,
        'categoria_actual': categoria_filtro
    })


def publicacion_detalle(request, id):
    publicacion = get_object_or_404(Publicacion, pk=id)
    comentarios = Comentario.objects.filter(publicacion=publicacion).select_related('usuario').order_by('fecha_creacion')
    reacciones = Reaccion.objects.filter(publicacion=publicacion).values('tipo_reaccion__nombre_tipo').annotate(total=Count('id_reaccion'))

    # Guarda comentario si es POST
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        usuario = Usuario.objects.first()  # ⚠️ temporal, reemplazar luego con request.user

        if contenido and usuario:
            Comentario.objects.create(
                contenido=contenido,
                usuario=usuario,
                publicacion=publicacion,
                categoria=publicacion.categoria
            )
            return redirect('publicacion_detalle', id=id)

    return render(request, 'detalle_publicacion.html', {
        'publicacion': publicacion,
        'comentarios': comentarios,
        'reacciones': reacciones
    })

def index(request):
    return render(request, 'index.html')

def registro(request):
    return render(request, 'registro.html')


def inicio_sesion(request):
    return render(request, 'inicio_sesion.html')

def mi_cuenta(request):
    return render(request, 'mi_cuenta.html')

def compra(request):
    return render(request, 'compra.html')

def pagar(request):
    return render(request, 'pagar.html')

def carrito(request):
    return render(request, 'carrito.html')