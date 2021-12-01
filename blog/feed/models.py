from django.db import models
from  django.contrib.auth.models import User
from PIL.Image  import Image

class categoria(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_fk = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=10 )
    foto= models.FileField(upload_to='fotos_perfil', default='fotos_perfil/foto_default.png')
    def __str__(self):
        return self.usuario_fk.username

class post(models.Model):
    posteador = models.ForeignKey(usuario, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    pre_contenido = models.TextField()
    categoria = models.ManyToManyField(categoria,  default=1)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    me_gusta = models.IntegerField(default=0)
    no_megusta = models.IntegerField(default=0)
    imagen = models.FileField(upload_to='imagenes_posts', default='feed/static/images/post_default.jpg')
    visitas = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

class comentario(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    comentador = models.ForeignKey(usuario, on_delete=models.CASCADE, null=True)
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    def __str__(self):
        salida = '{} {} {} {} {}'.format(self.id, self.post, self.comentador, self.contenido, self.creado_en)
        return salida


