from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Publicacion, Comentario, Reaccion, TipoReaccion, Categoria
from .models import Reaccion
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required





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

    # Registrar nuevo comentario
    if request.method == 'POST' and request.user.is_authenticated:
        contenido = request.POST.get('contenido')
        if contenido:
            Comentario.objects.create(
                contenido=contenido,
                usuario=request.user,
                publicacion=publicacion,
                categoria=publicacion.categoria
            )
            return redirect('publicacion_detalle', id=id)

    # Recuento total de reacciones por tipo
    reacciones_total = Reaccion.objects.filter(publicacion=publicacion).values('tipo_reaccion__nombre_tipo').annotate(total=Count('id_reaccion'))
    conteo_reacciones = {
        publicacion.id_publicacion: {
            r['tipo_reaccion__nombre_tipo']: r['total'] for r in reacciones_total
        }
    }

    # Reacciones del usuario actual para esta publicación
    reacciones_usuario = {}
    if request.user.is_authenticated:
        user_reacciones = Reaccion.objects.filter(usuario=request.user, publicacion=publicacion)
        for r in user_reacciones:
            reacciones_usuario.setdefault(r.publicacion.id_publicacion, set()).add(r.tipo_reaccion.nombre_tipo)

    # Reacciones por comentario
    comentarios_reacciones = {}
    for c in comentarios:
        likes = c.reacciones.filter(tipo_reaccion__nombre_tipo='Like').count()
        dislikes = c.reacciones.filter(tipo_reaccion__nombre_tipo='Dislike').count()
        comentarios_reacciones[c.id_comentario] = {'Like': likes, 'Dislike': dislikes}

    return render(request, 'detalle_publicacion.html', {
        'publicacion': publicacion,
        'comentarios': comentarios,
        'conteo_reacciones': conteo_reacciones,
        'reacciones_usuario': reacciones_usuario,
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

@csrf_exempt
def reaccion_ajax(request):
    if request.method == 'POST' and request.user.is_authenticated:
        pub_id = request.POST.get('publicacion_id')
        tipo_nombre = request.POST.get('tipo')

        try:
            publicacion = Publicacion.objects.get(pk=pub_id)
            tipo = TipoReaccion.objects.get(nombre_tipo=tipo_nombre)

            reaccion_existente = Reaccion.objects.filter(
                usuario=request.user,
                publicacion=publicacion,
                tipo_reaccion=tipo
            ).first()

            user_reaccion = None
            if reaccion_existente:
                reaccion_existente.delete()
            else:
                Reaccion.objects.create(usuario=request.user, publicacion=publicacion, tipo_reaccion=tipo)
                user_reaccion = tipo.nombre_tipo

            likes = Reaccion.objects.filter(publicacion=publicacion, tipo_reaccion__nombre_tipo='Like').count()
            dislikes = Reaccion.objects.filter(publicacion=publicacion, tipo_reaccion__nombre_tipo='Dislike').count()

            return JsonResponse({
                'success': True,
                'likes': likes,
                'dislikes': dislikes,
                'user_reaccion': user_reaccion
            })

        except:
            return JsonResponse({'success': False, 'error': 'Error al procesar la reacción'})

    return JsonResponse({'success': False, 'error': 'Solicitud inválida'})


@login_required
def mi_cuenta(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nueva_contrasena = request.POST.get('password1')
        confirmar_contrasena = request.POST.get('password2')


        if username:
            user.username = username
        if email:
            user.email = email

        if nueva_contrasena:
            if nueva_contrasena == confirmar_contrasena:
                user.set_password(nueva_contrasena)
                update_session_auth_hash(request, user)
            else:
                messages.error(request, '❌ Las contraseñas no coinciden.')
                return redirect('mi_cuenta')

        user.save()
        messages.success(request, '✅ Cambios guardados correctamente.')
        return redirect('mi_cuenta')

    return render(request, 'mi_cuenta.html', {'user': user})


def compra(request):
    return render(request, 'compra.html')



def recuperar_contrasena(request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        # Aquí podrías validar si el correo existe en User si lo deseas
        messages.success(request, "📩 Si el correo ingresado está vinculado a una cuenta en The Forest Wiki, recibirás un email con instrucciones.")
        return redirect('inicio_sesion')

    
    return render(request, 'password_olvidada.html')


def pagar(request):
    return render(request, 'pagar.html')


def carrito(request):
    return render(request, 'carrito.html')