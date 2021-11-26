
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from feed import views
urlpatterns = [
    path('', views.feed, name='feed'),
    path('registrarse/',views.registrarse, name='registrarse'),
    path('registrarse/crear_usuario/',views.crear_usuario, name='crear_usuario'),
    path('iniciar_sesion/',views.iniciar_sesion, name='iniciar_sesion'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('agregar_post',views.agregar_post, name='agregar_post'),

]