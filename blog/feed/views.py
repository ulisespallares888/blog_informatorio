from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.contrib import messages
from feed.models import *


def feed(request):
    posteos = post.objects.all()
    return render(request,"feed.html",{'posteos':posteos})

def registrarse(request):
    return render(request,"registrarse.html")

def login(request):
    return render(request,"login.html")


def crear_usuario(request):
    nombre = request.POST['txtnombre']
    email = request.POST['txtemail']
    password = request.POST['txtpassword']
    password2 = request.POST['txtpassword2']
    rol = request.POST['txtrol']

    if nombre != "" and email != "" and password != "" and password2 != "" and rol != "":
        usename_exists = User.objects.filter(username=nombre).exists()
        if usename_exists:
            messages.warning(request, 'El usuario ya existe')
        else:
            if password == password2:
                usuario_creado = User.objects.create(username=nombre,email=email,password=password)
                usuario_creado.save()
                usuario_rol = usuario.objects.create(usuario_fk_id=usuario_creado.id ,tipo_usuario=rol)
                usuario_rol.save()
                messages.success(request, 'Usuario creado correctamente')
                return redirect('login')
            else:
                messages.warning(request, 'Las contraseñas no coinciden')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('registrarse')


def iniciar_sesion(request):
    username = request.POST['txtusuario']
    password = request.POST['txtpassword']
    if username != "" and password !="":
        usuario_existe = User.objects.filter(username=username).exists()
        if usuario_existe:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}')
                return redirect('feed')
            else:
                messages.warning(request, 'Usuario o contraseña incorrectos')
        else:
            messages.warning(request, 'Usuario no existe')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('login')

