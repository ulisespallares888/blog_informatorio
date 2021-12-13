
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
    path('crear_comentario/<id>',views.crear_comentario, name='crear_comentario'),
    path('iniciar_sesion/',views.iniciar_sesion, name='iniciar_sesion'),
    path('leer_posteo/<id>',views.leer_posteo, name='leer_posteo'),
    path('buscar_por_catetoria/<id>',views.buscar_por_catetoria, name='buscar_por_catetoria'),
    path('busqueda_por_comentario',views.busqueda_por_comentario, name='busqueda_por_comentario'),
    path('busqueda_por_fecha',views.busqueda_por_fecha, name='busqueda_por_fecha'),
    path('busqueda_por_titulo',views.busqueda_por_titulo, name='busqueda_por_titulo'),
    path('reaccionar/<id>/<reac>',views.reaccionar, name='reaccionar'),
    path('nosotros/',views.nosotros, name='nosotros'),
    path('los_17_ods/',views.los_17_ods, name='los_17_ods'),
    path('accounts/',include('django.contrib.auth.urls')), 
    path('abrir_notificacion/<id>', views.abrir_notificacion, name='abrir_notificacion'),
    #path('mostar_comentarios/',views.mostar_comentarios, name='mostar_comentarios'),
]