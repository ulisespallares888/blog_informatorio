import contextlib
from typing import ContextManager
from django.db.models.expressions import F, Subquery
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
    notif_user = notificaciones.objects.filter(post__posteador_id=request.user.id).exclude(usuario_id = request.user.id).order_by('creado_en').reverse()[:10]
    notif_no_leidas = notificaciones.objects.filter(post__posteador_id=request.user.id, leido=False).exclude(usuario_id = request.user.id).exists()
    posteos = post.objects.all().order_by('creado_en').reverse() 
    categorias = categoria.objects.all()
    top_posts = post.objects.all().order_by('me_gusta').reverse()[:10]
    contexto={'posteos':posteos,'categorias':categorias,'notif_user':notif_user,'top_posts':top_posts,'notif_no_leidas':notif_no_leidas}
    return render(request,"feed.html",contexto)

def nosotros(request):
    return render(request,"nosotros.html")

def los_17_ods(request):
    return render(request,"que_son_los_17_ods.html")

def leer_posteo(request,id):
    un_posteo=post.objects.get(id=id)
    un_posteo.visitas += 1
    un_posteo.save()
    comentarios_del_posteo = comentario.objects.filter(post_id=id,aprobado=True).order_by('creado_en').reverse()
    usuarios_user = User.objects.filter(id__in=comentarios_del_posteo.values('comentador_id'))
    usuarios = usuario.objects.filter(usuario_fk_id__in=usuarios_user.values('id'))
    contexto = {'un_posteo':un_posteo,'comentarios_del_posteo':comentarios_del_posteo,'usuarios':usuarios}
    return render(request,"leer_post.html",contexto)

@login_required
def abrir_notificacion(request,id):
    
    notif = notificaciones.objects.filter(post_id=id).first()
    print(notif)
    notif.leido = True
    notif.save()
    return redirect('leer_posteo',id)

@login_required
def agregar_post(request):
    tipo_usuario_actual = usuario.objects.get(usuario_fk_id=request.user.id)
    if tipo_usuario_actual.tipo_usuario_id == 2:
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
    else:
        messages.warning(request, 'No tienes permisos para crear un posteos, registrate como usuario Postador')
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
def crear_comentario(request,id):
    contenido = request.GET.get('txtcontenido')
    nueva_notif = notificaciones.objects.create(usuario_id=request.user.id, nombre_usuario=request.user.username,  post_id=id, comentario = True)
    nueva_notif.save()
    if comentario != "" and contenido != "":
        comentario_creado = comentario.objects.create(contenido=contenido, comentador=request.user, post_id=id,nombre_comentador=request.user.username)
        comentario_creado.save()
        messages.success(request, 'El comentario ha sido creado correctamente espere que el administrador lo apruebe')
    else:
        messages.warning(request, 'Hay campos vacios')

    return redirect('leer_posteo',id)


@login_required
def perfil_usuario(request):
    notif_user = notificaciones.objects.filter(post__posteador_id=request.user.id ).exclude(usuario_id = request.user.id).order_by('creado_en').reverse()[:10]
    mis_posteos = post.objects.filter(posteador_id=request.user.id).order_by('creado_en').reverse()
    mis_categorias = categoria.objects.filter(id__in = mis_posteos.values('categoria_id'))
    mis_comentarios = comentario.objects.filter(comentador_id=request.user.id).order_by('creado_en').reverse()
    posteos = post.objects.filter(comentario__comentador_id=request.user.id).distinct()
    categorias = categoria.objects.all()
    usuario_actual = usuario.objects.get( usuario_fk_id =request.user.id)
    contexto = {'mis_posteos':mis_posteos, 'mis_comentarios':mis_comentarios, 'categorias':categorias, 'notif_user':notif_user, 'mis_categorias':mis_categorias, 'usuario_actual':usuario_actual, 'posteos':posteos}
    return render(request,"mi_contenido.html",contexto)

def buscar_por_catetoria(request,id):
    posteos = post.objects.filter(categoria_id=id).order_by('creado_en').reverse()
    categorias = categoria.objects.all()
    top_posts = post.objects.all().order_by('me_gusta').reverse()[:10]
    notif_user = notificaciones.objects.filter(post__posteador_id=request.user.id ).exclude(usuario_id = request.user.id).order_by('creado_en').reverse()[:10]
    notif_no_leidas = notificaciones.objects.filter(post__posteador_id=request.user.id, leido=False).exclude(usuario_id = request.user.id).exists()
    contexto = {'posteos':posteos, 'categorias':categorias, 'top_posts':top_posts, 'notif_user':notif_user, 'notif_no_leidas':notif_no_leidas}
    return render(request,"feed.html",contexto)
    
def busqueda_por_fecha(request):
    fecha_bus = request.GET.get('fecha_buscada')
    posteos = post.objects.filter(creado_en__contains=fecha_bus).order_by('creado_en').reverse()
    categorias = categoria.objects.all()
    top_posts = post.objects.all().order_by('me_gusta').reverse()[:10]
    notif_user = notificaciones.objects.filter(post__posteador_id=request.user.id ).exclude(usuario_id = request.user.id).order_by('creado_en').reverse()[:10]
    notif_no_leidas = notificaciones.objects.filter(post__posteador_id=request.user.id, leido=False).exclude(usuario_id = request.user.id).exists()
    contexto = {'posteos':posteos, 'categorias':categorias, 'top_posts':top_posts, 'notif_user':notif_user, 'notif_no_leidas':notif_no_leidas}
    return render(request,"feed.html",contexto)

def busqueda_por_comentario(request):
    comentario_bus = request.GET.get('comentario_buscado')
    categorias = categoria.objects.all()
    posteos = post.objects.filter(comentario__contenido__contains=comentario_bus).distinct().order_by('creado_en').reverse()
    top_posts = post.objects.all().order_by('me_gusta').reverse()[:10]
    notif_user = notificaciones.objects.filter(post__posteador_id=request.user.id ).exclude(usuario_id = request.user.id).order_by('creado_en').reverse()[:10]
    notif_no_leidas = notificaciones.objects.filter(post__posteador_id=request.user.id, leido=False).exclude(usuario_id = request.user.id).exists()
    contexto = {'posteos':posteos, 'categorias':categorias, 'top_posts':top_posts, 'notif_user':notif_user, 'notif_no_leidas':notif_no_leidas}
    return render(request,"feed.html",contexto)

def busqueda_por_titulo(request):
    titulo_bus = request.GET.get('titulo_buscado')
    categorias = categoria.objects.all()
    top_posts = post.objects.all().order_by('me_gusta').reverse()[:10]
    posteos = post.objects.filter(titulo__contains=titulo_bus).order_by('creado_en').reverse()
    contexto = {'posteos':posteos,'categorias':categorias,'top_posts':top_posts}
    return render(request,"feed.html",contexto)

#---------------------------------------------------------------------------------------------------
#                                     VISTAS PARA EL TRECER SPRINT
#---------------------------------------------------------------------------------------------------


@login_required
def eliminar_post(request,id):
    post_eliminado = post.objects.get(id=id)
    post_eliminado.delete()
    messages.success(request, 'El post {} ha sido eliminado correctamente'.format(post_eliminado.titulo))
    return redirect('perfil_usuario')

@login_required
def editar_post(request,id):
    post_editar = post.objects.get(id=id)
    categorias = categoria.objects.all()
    contexto = {'post_editar':post_editar, 'categorias':categorias}
    return render(request,"editar_post.html",contexto)


@login_required
def editar_post_guardar(request,id):
    titulo = request.POST.get('txttitulo',"titulo_nada")
    contenido = request.POST.get('txtcontenido',"contenido_nada")
    categoria = request.POST.get('txtcategoria',"categoria_nada")
    if titulo != "" and contenido != "":
        post_editar = post.objects.get(id=id)
        post_editar.titulo = titulo
        post_editar.contenido = contenido
        post_editar.pre_contenido = contenido[:200]
        post_editar.catetoria_id = categoria
        post_editar.save()
    
        messages.success(request, 'Post editado correctamente')
    else:
        messages.warning(request, 'Hay campos vacios')
    return redirect('perfil_usuario')
    #return redirect('editar_post',id)



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
    return redirect('leer_posteo',id)

@login_required
def editar_perfil(request,id):
    user_editar = User.objects.get(id=id)
    usuario_editar = usuario.objects.get(usuario_fk_id=id)
    contexto = {'user_editar':user_editar,'usuario_editar':usuario_editar}
    return render(request,"editar_perfil.html",contexto)

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



    