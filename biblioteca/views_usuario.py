from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Publicacion, Comentario, Reaccion, TipoReaccion, Categoria
from .models import Reaccion
from django.db.models import Count



def cerrar_sesion(request):
    logout(request)
    return redirect('index')


def foro(request):
    categoria_filtro = request.GET.get('categoria')
    categorias = Categoria.objects.all()

    if categoria_filtro and categoria_filtro.lower() != 'todo':
        publicaciones = Publicacion.objects.select_related('usuario', 'categoria').filter(
            categoria__nombre_categoria__iexact=categoria_filtro
        ).order_by('-fecha_creacion')
    else:
        publicaciones = Publicacion.objects.select_related('usuario', 'categoria').order_by('-fecha_creacion')

    if request.method == 'POST' and request.user.is_authenticated:
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        categoria_id = request.POST.get('categoria')
        usuario = request.user

        if contenido and categoria_id and usuario:
            categoria = Categoria.objects.get(pk=categoria_id)
            Publicacion.objects.create(
    titulo=titulo,
    contenido=contenido,
    usuario=usuario,
    categoria=categoria
)
            return redirect('foro')

    # Conteo de reacciones agrupadas por publicación y tipo
    reacciones = Reaccion.objects.values('publicacion_id', 'tipo_reaccion__nombre_tipo').annotate(total=Count('id_reaccion'))
    conteo_reacciones = {}
    for reaccion in reacciones:
        pub_id = reaccion['publicacion_id']
        tipo = reaccion['tipo_reaccion__nombre_tipo']
        conteo_reacciones.setdefault(pub_id, {})[tipo] = reaccion['total']

    return render(request, 'foro.html', {
        'publicaciones': publicaciones,
        'categoria_actual': categoria_filtro,
        'categorias': categorias,
        'conteo_reacciones': conteo_reacciones
    })


def publicacion_detalle(request, id):
    publicacion = get_object_or_404(Publicacion, pk=id)
    comentarios = Comentario.objects.filter(publicacion=publicacion).select_related('usuario').order_by('fecha_creacion')
    reacciones = Reaccion.objects.filter(publicacion=publicacion).values('tipo_reaccion__nombre_tipo').annotate(total=Count('id_reaccion'))

    if request.method == 'POST' and request.user.is_authenticated:
        contenido = request.POST.get('contenido')
        usuario = request.user

        if contenido and usuario:
            Comentario.objects.create(
                contenido=contenido,
                usuario=usuario,
                publicacion=publicacion,
                categoria=publicacion.categoria
            )
            return redirect('publicacion_detalle', id=id)

    comentarios_reacciones = {}
    for c in comentarios:
        likes = c.reacciones.filter(tipo_reaccion__nombre_tipo='Like').count()
        dislikes = c.reacciones.filter(tipo_reaccion__nombre_tipo='Dislike').count()
        comentarios_reacciones[c.id_comentario] = {'Like': likes, 'Dislike': dislikes}

    return render(request, 'detalle_publicacion.html', {
        'publicacion': publicacion,
        'comentarios': comentarios,
        'reacciones': reacciones,
        'comentarios_reacciones': comentarios_reacciones
    })


def index(request):
    return render(request, 'index.html')


def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('usuario')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        confirmar = request.POST.get('confirmar')

        if contrasena != confirmar:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro')

        if User.objects.filter(username=nombre).exists():
            messages.error(request, 'Este nombre de usuario ya está en uso.')
            return redirect('registro')

        if User.objects.filter(email=correo).exists():
            messages.error(request, 'Este correo ya está registrado.')
            return redirect('registro')

        User.objects.create_user(username=nombre, email=correo, password=contrasena)

        messages.success(request, '✅ Usuario registrado correctamente. ¡Ahora puedes iniciar sesión!')
        return redirect('inicio_sesion')

    return render(request, 'registro.html')


def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('contrasena')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, '❌ Usuario o contraseña incorrectos.')

    return render(request, 'inicio_sesion.html')


def mi_cuenta(request):
    return render(request, 'mi_cuenta.html')


def compra(request):
    return render(request, 'compra.html')


def pagar(request):
    return render(request, 'pagar.html')


def carrito(request):
    return render(request, 'carrito.html')