from django.db import models
from  django.contrib.auth.models import User
from PIL.Image  import Image


class tipo_usuario(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class categoria(models.Model):
    name = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='categoria',default='categoria_default.png')
    def __str__(self):
        return self.name

class usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_fk = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.ForeignKey(tipo_usuario, on_delete=models.CASCADE, null=False)
    foto= models.FileField(upload_to='fotos_perfil', default='foto_default.jpg')
    def __str__(self):
        return self.usuario_fk.username

class post(models.Model):
    posteador = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    pre_contenido = models.TextField()
    categoria = models.ForeignKey(categoria, on_delete=models.CASCADE,  default=1, null=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    me_gusta = models.IntegerField(default=0)
    no_megusta = models.IntegerField(default=0)
    imagen = models.FileField(upload_to='imagenes_posts', default='post_default.jpg')
    visitas = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

class comentario(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    comentador = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    aprobado = models.BooleanField(default=False)
    def __str__(self):
        salida = '{} {} {} {} {}'.format(self.id, self.post, self.comentador, self.contenido, self.creado_en)
        return salida


class reaccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    me_gusta = models.BooleanField(default=False)
    no_megusta = models.BooleanField(default=False)
    def __str__(self):
        return '{} {}'.format(self.usuario, self.post)


class notificaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_usuario = models.CharField(max_length=50, default=None)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    leido = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    comentario=models.BooleanField(default=False)
    me_gusta=models.BooleanField(default=False)
    no_megusta=models.BooleanField(default=False)
    def __str__(self):
        return '{} {} {}'.format(self.usuario, self.post, self.leido)