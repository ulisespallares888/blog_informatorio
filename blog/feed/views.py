from django.db.models.fields import DateTimeCheckMixin, DateTimeField
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from feed.models import *
import datetime




#---------------------------------------------------------------------------------------------------
#                                    VISTAS PARA EL PRIMER SPRINT
#---------------------------------------------------------------------------------------------------


def feed(request):
    notif_user = notificaciones.objects.filter(post__posteador_id=request.user.id ).exclude(usuario_id = request.user.id).order_by('creado_en').reverse()
    posteos = post.objects.all().order_by('creado_en').reverse() 
    categorias = categoria.objects.all()
    print(notif_user,len(notif_user))
    contexto={'posteos':posteos,'categorias':categorias,'notif_user':notif_user}
    return render(request,"feed.html",contexto)

def leer_posteo(request,id):
    un_posteo=post.objects.get(id=id)
    comentarios_del_posteo = comentario.objects.filter(post_id=id)
    un_posteo.visitas += 1
    un_posteo.save()
    return render(request,"leer_post.html",{'un_posteo':un_posteo, 'comentarios_del_posteo':comentarios_del_posteo})

#agragar bien el tipo_17_ods
@login_required
def agregar_post(request):
    titulo = request.POST['txttitulo']
    contenido = request.POST['txtcontenido']
    imagen = request.FILES.get('txtimagen','post_default.jpg')
    categoria_match = request.POST.get('txtcategoria')
    pre_contenido = str(contenido)[0:60] + "[...]"
    usuario_match = User.objects.get(id = request.user.id)
    if titulo != "" and contenido != "":
        post_creado = post.objects.create(titulo=titulo,contenido=contenido,posteador=usuario_match,pre_contenido=pre_contenido, categoria_id=categoria_match,imagen=imagen)
        post_creado.save()
        messages.success(request, 'Post creado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('perfil_usuario')


def registrarse(request):
    tipo_usuario_match = tipo_usuario.objects.all()
    return render(request,"registrarse.html",{'tipo_usuario_match':tipo_usuario_match})


def crear_usuario(request):
    nombre = request.POST['txtnombre']
    email = request.POST['txtemail']
    password = request.POST['txtpassword']
    password2 = request.POST['txtpassword2']
    rol = request.POST.get('txttrol')
    foto = request.FILES.get('txtimagen','foto_default.jpg')
    if nombre != "" and email != "" and password != "" and password2 != "" and rol != "":
        usename_exists = User.objects.filter(username=nombre).exists()
        if usename_exists:
            messages.warning(request, 'El usuario ya existe')
        else:
            if password == password2:
                usuario_creado = User.objects.create_user(username=nombre,email=email,password=password)
                usuario_creado.save()
                usuario_rol = usuario.objects.create(usuario_fk_id=usuario_creado.id ,tipo_usuario_id=rol,foto=foto)
                usuario_rol.save()
                messages.success(request, 'Usuario creado correctamente')
                return redirect('acceder')
            else:
                messages.warning(request, 'Las contraseñas no coinciden')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('registrarse')


def acceder(request):
    return render(request,"registration/login.html")



#--------------arreglar el iniciar sesion en la parte-------------
def iniciar_sesion(request):
    nombre = request.POST['txtusuario']
    contrasenia = request.POST['txtpassword']
    if nombre != "" and contrasenia !="":
        usuario_existe = User.objects.filter(username=nombre).exists()
        if usuario_existe:
            user = authenticate(request, username=nombre, password=contrasenia)
            print(user)
            if user is not None:
                login(request,user)
                messages.success(request, f'Bienvenido {nombre}')
                return redirect('feed')
            else:
                messages.warning(request, 'Usuario y/o contraseña incorrectos')
        else:
            messages.warning(request, 'Usuario no existe')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('acceder')

#---------------------------------------------------------------------------------------------------
#                                     VISTAS PARA EL SEGUNDO SPRINT
#---------------------------------------------------------------------------------------------------

#configurar a que post va el comentario y por quien es creado
@login_required
def crear_comentario(request):
    contenido = request.POST['txtcontenido']
    usuario_match = usuario.objects.get(id=request.user.id)
    if comentario != "" and contenido != "":
        comentario_creado = comentario.objects.create(contenido=contenido, comentador=usuario_match, post_id=1)
        comentario_creado.save()
        messages.success(request, 'Comentario creado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')

    return redirect('leer_posteo',id)


@login_required
def perfil_usuario(request):
    posteos = post.objects.filter(posteador_id=request.user.id)
    comentarios = comentario.objects.filter(comentador_id=request.user.id)
    categorias = categoria.objects.all()
    return render(request,"perfil_usuario.html",{'posteos':posteos, 'comentarios':comentarios, 'categorias':categorias})


def buscar_por_catetoria(request,id):
    posteos = post.objects.filter(categoria_id=id).order_by('creado_en').reverse()
    categorias = categoria.objects.all()
    return render(request,"feed.html",{'posteos':posteos,'categorias':categorias})
    

def busqueda_por_fecha(request):
    fecha_bus = request.GET.get('fecha_buscada')
    print(fecha_bus)
    posteos = post.objects.filter(creado_en__contains=fecha_bus).order_by('creado_en').reverse()
    categorias = categoria.objects.all()
    return render(request,"feed.html",{'posteos':posteos,'categorias':categorias})

def busqueda_por_comentario(request):
    comentario_bus = request.GET.get('comentario_buscado')
    categorias = categoria.objects.all()
    posteos = post.objects.filter( comentario__contenido__contains=comentario_bus)
    return render(request,"feed.html",{'posteos':posteos,'categorias':categorias})



#---------------------------------------------------------------------------------------------------
#                                     VISTAS PARA EL TRECER SPRINT
#---------------------------------------------------------------------------------------------------


@login_required
def eliminar_post(request,id):
    post_eliminado = post.objects.get(id=id)
    post_eliminado.delete()
    messages.success(request, 'Post eliminado correctamente')
    return redirect('perfil_usuario')

@login_required
def editar_post(request,id):
    post_editar = post.objects.get(id=id)
    return render(request,"editar_post.html",{'post_editar':post_editar})


@login_required
def editar_post_guardar(request,id):
    titulo = request.POST['txttitulo']
    contenido = request.POST['txtcontenido']
    if titulo != "" and contenido != "":
        post_editar = post.objects.get(id=id)
        post_editar.titulo = titulo
        post_editar.contenido = contenido
        post_editar.save()
        messages.success(request, 'Post editado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('perfil_usuario')

@login_required
def eliminar_comentario(request,id):
    comentario_eliminado = comentario.objects.get(id=id)
    comentario_eliminado.delete()
    messages.success(request, 'Comentario eliminado correctamente')
    return redirect('perfil_usuario')



#---------------------------------------------------------------------------------------------------
#                                     VISTAS PARA EL CUARTO SPRINT
#---------------------------------------------------------------------------------------------------
@login_required
def reaccionar(request,id,reac):
    reaccion_exists = reaccion.objects.filter(usuario_id=request.user.id,post_id=id).exists()
    post_reaccionar = post.objects.get(id=id)
    if not reaccion_exists:
        if reac == "mg":
            reaccion_creado = reaccion.objects.create(usuario_id=request.user.id,post_id=id,me_gusta=True,no_megusta=False)
            post_reaccionar.me_gusta += 1
        else:
            reaccion_creado = reaccion.objects.create(usuario_id=request.user.id,post_id=id,me_gusta=False,no_megusta=True)
            post_reaccionar.no_megusta += 1
        reaccion_creado.save()
        nueva_notif = notificaciones.objects.create(usuario_id=request.user.id, nombre_usuario=request.user,  post_id=id, me_gusta=reaccion_creado.me_gusta, no_megusta=reaccion_creado.no_megusta)

    else:
        reaccion_bus = reaccion.objects.get(usuario_id=request.user.id,post_id=id)
        if reac == "mg":
            if reaccion_bus.me_gusta == True and reaccion_bus.no_megusta == False:
                reaccion_bus.me_gusta=False
                reaccion_bus.no_megusta=False
                post_reaccionar.me_gusta -= 1
            elif reaccion_bus.me_gusta == False and reaccion_bus.no_megusta == False:
                reaccion_bus.me_gusta=True
                post_reaccionar.me_gusta += 1
            else:
                if reaccion_bus.me_gusta == False and reaccion_bus.no_megusta == True:
                    reaccion_bus.me_gusta=True
                    reaccion_bus.no_megusta=False
                    post_reaccionar.me_gusta += 1
                    post_reaccionar.no_megusta -= 1
        else:
            if reaccion_bus.me_gusta == True and reaccion_bus.no_megusta == False:
                reaccion_bus.me_gusta=False
                reaccion_bus.no_megusta=True
                post_reaccionar.me_gusta -= 1
                post_reaccionar.no_megusta += 1
            elif reaccion_bus.me_gusta == False and reaccion_bus.no_megusta == False:
                reaccion_bus.no_megusta=True
                post_reaccionar.no_megusta += 1
            else:
                if reaccion_bus.me_gusta == False and reaccion_bus.no_megusta == True:
                    reaccion_bus.no_megusta=False
                    post_reaccionar.no_megusta -= 1
        reaccion_bus.save()
        nueva_notif = notificaciones.objects.create(usuario_id=request.user.id, post_id=id, nombre_usuario=request.user,  me_gusta=reaccion_bus.me_gusta, no_megusta=reaccion_bus.no_megusta)
    post_reaccionar.save()
    messages.success(request, 'Reaccion realizada correctamente')
    return redirect('leer_posteo',id)

@login_required
def editar_perfil(request,id):
    usuario_editar = usuario.objects.get(id=id)
    return render(request,"editar_perfil.html")

@login_required
def editar_perfil_guardar(request,id):
    nombre = request.POST['txtnombre']
    email = request.POST['txtemail']
    foto = request.POST['txtfoto']
    if nombre != "" and email != "":
        usuario_editar = usuario.objects.get(id=id)
        usuario_editar.nombre = nombre
        usuario_editar.email = email
        usuario_editar.foto = foto
        usuario_editar.save()
        messages.success(request, 'Perfil editado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('perfil_usuario')