from django.db import models

class TipoUsuario(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_tipo


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    tipo_usuario = models.ForeignKey(
        TipoUsuario,
        on_delete=models.CASCADE,
        related_name="usuarios"
    )

    def __str__(self):
        return self.nombre_usuario


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_categoria


class Publicacion(models.Model):
    id_publicacion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="publicaciones"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="publicaciones"
    )

    def __str__(self):
        return self.titulo

class Juego(models.Model):
    id_juego = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre



class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comentarios"
    )

    def __str__(self):
        return f"Comentario de {self.usuario} en '{self.publicacion}'"


class TipoReaccion(models.Model):
    id_tipo_reaccion = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_tipo


class Reaccion(models.Model):
    id_reaccion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="reacciones"
    )
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name="reacciones"
    )
    tipo_reaccion = models.ForeignKey(
        TipoReaccion,
        on_delete=models.CASCADE,
        related_name="reacciones"
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'publicacion', 'tipo_reaccion')

    def __str__(self):
        return f"{self.tipo_reaccion} de {self.usuario} en '{self.publicacion}'"


class VersionJuego(models.Model):
    id_version = models.AutoField(primary_key=True)
    nombre_version = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre_version


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="ventas"
    )
    version = models.ForeignKey(
        VersionJuego,
        on_delete=models.CASCADE,
        related_name="ventas"
    )
    fecha_venta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id_venta}: {self.usuario} compró {self.version}"
