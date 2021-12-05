from django.contrib import admin
from feed.models import *

admin.site.register(post)
admin.site.register(comentario)
admin.site.register(usuario)
admin.site.register(categoria)
admin.site.register(tipo_usuario)
admin.site.register(reaccion)
admin.site.register(notificaciones)