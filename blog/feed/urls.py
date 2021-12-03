
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from feed import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.feed, name='feed'),
    path('acceder',views.acceder, name='acceder'),
    path('registrarse/',views.registrarse, name='registrarse'),
    path('registrarse/crear_usuario/',views.crear_usuario, name='crear_usuario'),
    path('iniciar_sesion/',views.iniciar_sesion, name='iniciar_sesion'),
    path('perfil_usuario/agregar_post/',views.agregar_post, name='agregar_post'),
    path('eliminar_post/<id>',views.eliminar_post, name='eliminar_post'),
    path('perfil_usuario/',views.perfil_usuario, name='perfil_usuario'),
    path('crear_comentario/',views.crear_comentario, name='crear_comentario'),
    path('iniciar_sesion/',views.iniciar_sesion, name='iniciar_sesion'),
    path('leer_posteo/<id>',views.leer_posteo, name='leer_posteo'),
    path('buscar_por_catetoria/<id>',views.buscar_por_catetoria, name='buscar_por_catetoria'),
    path('reaccionar/<id>/<reac>',views.reaccionar, name='reaccionar'),
    path('accounts/',include('django.contrib.auth.urls')),
    
    
    #path('mostar_comentarios/',views.mostar_comentarios, name='mostar_comentarios'),
   
]