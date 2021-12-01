from django.db import models
from  django.contrib.auth.models import User
from PIL.Image  import Image

tipos = [
    ('Fin de la pobreza',1),
    (2,'Hambre cero'),
    (3,'Salud y bienestar'),
    (4,'Educación de calidad'),
    (5,'Igualdad de género'),
    (6,'Agua limpia y saneamiento'),
    (7,'Energía asequible y no contaminante'),
    (8,'Trabajo y crecimiento económico'),
    (9,'Industria, innovación e infraestructura'),
    (10,'Reducción de las desigualdades'),
    (11,'Ciudades y comunidades sostenibles'),
    (12,'Producción y consumo responsables'),
    (13,'Acción por el clima'),
    (14,'Vida submarina'),
    (15,'Vida de ecosistemas terrestres'),
    (16,'Paz y justicia para todos'),
    (17,'Alianzas para lograr los objetivos'),
    ]

class usuario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_fk = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=10 )
    #imagen = models.ImageField(upload_to='perfil_usuario', blank=True, null=True)

    def __str__(self):
        return self.usuario_fk.username

class post(models.Model):
    posteador = models.ForeignKey(usuario, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    pre_contenido = models.TextField()
    tipo_17_ODS= models.CharField( choices=tipos , max_length=50, default=1)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    me_gusta = models.IntegerField(default=0)
    no_megusta = models.IntegerField(default=0)
    imagen = models.FileField(upload_to='imagenes_posts', default='feed/static/images/default.jpg')
    visitas = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo

class comentario(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    comentador = models.ForeignKey(usuario, on_delete=models.CASCADE, null=True)
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    #me_gusta = models.IntegerField(default=0)
    #no_megusta = models.IntegerField(default=0)
    def __str__(self):
        salida = '{} {} {} {} {}'.format(self.id, self.post, self.comentador, self.contenido, self.creado_en)
        return salida


