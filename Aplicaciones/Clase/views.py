from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Clase, CustomUser, Material, Tarea, Entrega, Retroalimentacion
from django.contrib import messages

#import re

#from .models import Clase, 
# Create your views here.
#def inicio(request):
#    return render(request,'inicio.html')
#def signup(request):
#    if request.method == 'GET':
#        return render(request, 'signup.html'),{
#            'form': UserCreationForm
#       })
#    else:
#        if request.


def inicio(request):
    if request.method == 'POST':
        if 'registro' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            es_maestro = 'es_maestro' in request.POST
            maestro_password = request.POST.get('maestro_password', '')

            # Validaciones
            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden.')
            elif CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'El correo ya está registrado.')
            elif es_maestro and maestro_password != '@dminM77':
                messages.error(request, 'Contraseña de maestro incorrecta.')
            else:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password1,
                    es_maestro=es_maestro
                )
                login(request, user)
                messages.success(request,"Registro exitoso")
                return redirect('inicio')

        elif 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request,"Correcto Inicio de Sesion")

                return redirect('dashboard_maestro' if user.es_maestro else 'dashboard_estudiante')

    return render(request, 'inicio.html')

#Cerrar Sesion
def signout(request):
    logout(request)
    return redirect('inicio')

@login_required
def dashboard_maestro(request):
    if not request.user.es_maestro:
        return redirect('dashboard_estudiante')
    clases = request.user.clases.all()
    return render(request, 'dashboard_maestro.html', {'clases': clases})

@login_required
def dashboard_estudiante(request):
    if request.user.es_maestro:
        return redirect('dashboard_maestro')
    clases = Clase.objects.all()
    return render(request, 'dashboard_estudiante.html', {'clases': clases})

@login_required
def nuevaClase(request):
    return render(request,'nuevaClase.html')

#Presentando en Pantalla el listado de clases  (accesible por maestros y estudiantes)
@login_required
def listadoClase(request):
    clasesBdd = Clase.objects.all()
    return render(request, 'listadoClase.html', {'clases': clasesBdd, 'es_maestro': request.user.es_maestro})

@login_required
def detalleClase(request, id):
    clase = get_object_or_404(Clase, id=id)

    if request.user.es_maestro and clase.maestro != request.user:
        return redirect('error')  

    es_maestro = request.user.es_maestro
    context = {
        'clase': clase,
        'es_maestro': es_maestro,
    }
    return render(request, 'detalleClase.html', context)

@login_required
def guardarClase(request):
    if not request.user.es_maestro:
        return redirect('/')

    if request.method == "POST":
        titulo = request.POST.get('txt_titulo', '').strip()
        descripcion = request.POST.get('txt_descripcion', '').strip()
        maestro_id = request.POST.get('txt_maestro', '').strip()
        video_url = request.POST.get('txt_video_url', '').strip()
        fecha_publicacion = request.POST.get('txt_fecha_publicacion', '').strip()
        
        try:
            maestro = CustomUser.objects.get(id=maestro_id, es_maestro=True)
        except CustomUser.DoesNotExist:
            messages.error(request, "El maestro especificado no existe o no es válido.")
            return redirect('/nuevaClase')

        nueva_clase = Clase.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            maestro=maestro,
            video_url=video_url,
            fecha_publicacion=fecha_publicacion
        )
        messages.success(request,"Clase guardada correctamente")
        return redirect('/dashboard_maestro')  
    
    maestros = CustomUser.objects.filter(es_maestro=True)
    return render(request, 'nuevaClase.html', {'maestros': maestros})

# Convertir url 
#def convertir_url_youtube(url):
#    """
#    Convierte una URL normal de YouTube en una URL embed.
#    """
#    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/)?(?P<id>[a-zA-Z0-9_-]{11})'
#    if match:
#    match = re.match(youtube_regex, url)
#        video_id = match.group('id')
#        return f"https://www.youtube.com/embed/{video_id}"
#    return url

@login_required
def eliminarClase(request,id):
    claseEliminar=Clase.objects.get(id=id)
    claseEliminar.delete()
    messages.success(request,"Clase eliminada correctamente")
    return redirect('/dashboard_maestro')

#Funcion para mostrar el formulario de edicion
@login_required
def editarClase(request,id):
    claseEditar=Clase.objects.get(id=id)
    return render(request,'editarClase.html',
                  {'clase':claseEditar})

def procesarEdicionClase(request):
    if not request.user.es_maestro:
        return redirect('/')

    try:
        clase = Clase.objects.get(id=request.POST['id'], maestro=request.user)
    except Clase.DoesNotExist:
        messages.error(request, "La clase especificada no existe o no tienes permiso para editarla.")
        return redirect('/dashboard_maestro')

    if request.method == "POST":
        titulo = request.POST.get('txt_titulo', '').strip()
        descripcion = request.POST.get('txt_descripcion', '').strip()
        video_url = request.POST.get('txt_video_url', '').strip()
        fecha_publicacion = request.POST.get('txt_fecha_publicacion', '').strip()

        clase.titulo = titulo
        clase.descripcion = descripcion
        clase.video_url = video_url
        clase.fecha_publicacion = fecha_publicacion
        clase.save()

        messages.success(request, "Clase actualizada correctamente.")
        return redirect('/dashboard_maestro')
    return render(request, 'editarClase.html', {'clase': clase})

# Tbl Material: Agregar material (solo maestros)
@login_required
def nuevoMaterial(request, clase_id):
    if not request.user.es_maestro:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción. Solo maestros")
    
    clase = get_object_or_404(Clase, id=clase_id)
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion', '')
        archivo = request.FILES.get('archivo')
        if titulo and archivo:
            Material.objects.create(clase=clase, titulo=titulo, descripcion=descripcion, archivo=archivo)
            messages.success(request,"Material agregado correctamente")

            return redirect('listadoClase')
    return render(request, 'nuevoMaterial.html', {'clase': clase})

# Ver materiales de una clase (maestros y estudiantes)
@login_required
def verMaterial(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    materiales = clase.materiales.all()
    return render(request, 'verMaterial.html', {'clase': clase, 'materiales': materiales})

@login_required
def editarMaterial(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    # Verificar que el usuario sea maestro
    if not request.user.es_maestro:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == "POST":
        material.titulo = request.POST.get('titulo')
        material.descripcion = request.POST.get('descripcion')
        
        archivo = request.FILES.get('archivo')
        if archivo:
            material.archivo = archivo

        material.save()
        messages.success(request,"Material editado correctamente")
        return redirect('listadoClase')

    return render(request, 'editarMaterial.html', {'material': material})

@login_required
def eliminarMaterial(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if not request.user.es_maestro:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == "POST":
        material.delete()
        messages.success(request,"Material eliminado correctamente")

        return redirect('listadoClase')

    return render(request, 'eliminarMaterial.html', {'material': material})

@login_required
def detalleMaterial(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, 'detalleMaterial.html', {'material': material})

# Tbl Tarea : gregar nueva tarea (solo maestros)
@login_required
def nuevaTarea(request, clase_id):
    if not request.user.es_maestro:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    
    clase = get_object_or_404(Clase, id=clase_id)
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion', '')
        fecha_entrega = request.POST.get('fecha_entrega')
        if titulo and fecha_entrega:
            Tarea.objects.create(clase=clase, titulo=titulo, descripcion=descripcion, fecha_entrega=fecha_entrega)
            messages.success(request,"Tarea agregada correctamente")
            return redirect('listadoClase')
    return render(request, 'nuevaTarea.html', {'clase': clase})

@login_required
def listaTareas(request, clase_id):
    # Obtener la clase específica
    clase = get_object_or_404(Clase, id=clase_id)
    tareas = Tarea.objects.filter(clase=clase)

    return render(request, 'listaTareas.html', {'clase': clase, 'tareas': tareas})

# Ver tareas de una clase (maestros y estudiantes)
@login_required
def verTareas(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    tareas = clase.tareas.all()
    return render(request, 'verTareas.html', {'clase': clase, 'tareas': tareas, 'es_maestro': request.user.es_maestro})

@login_required
def editarTarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    # Verificación: Es maestro
    if not request.user.es_maestro:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == "POST":
        tarea.titulo = request.POST.get("titulo")
        tarea.descripcion = request.POST.get("descripcion")
        tarea.fecha_entrega = request.POST.get("fecha_entrega")
        tarea.save()
        messages.success(request,"Tarea editada correctamente")

        return redirect('listaTareas', tarea.clase.id)

    return render(request, 'editarTarea.html', {'tarea': tarea})

@login_required
def eliminarTarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    # Verificación: Es maestro
    if not request.user.es_maestro:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == "POST":
        tarea.delete()
        messages.success(request,"Tarea eliminadas correctamente")

        return redirect('listaTareas', tarea.clase.id)

    return render(request, 'eliminarTarea.html', {'tarea': tarea})

# ENTREGAS
@login_required
def detalleTarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if not request.user.es_maestro:
        return HttpResponseForbidden("Solo los maestros pueden ver los detalles de la tarea.")

    entregas = tarea.entregas.all()

    return render(request, "detalleTarea.html", {
        "tarea": tarea,
        "entregas": entregas,
    })

#Solo estudiante  BORRAR--
@login_required
def subirTarea(request, tarea_id):
    if request.method == "POST":
        tarea = get_object_or_404(Tarea, id=tarea_id)
        comentario = request.POST.get("comentario", "")
        archivo = request.FILES.get("archivo", None)

        entrega = Entrega.objects.create(
            tarea=tarea,
            estudiante=request.user,
            comentario=comentario,
            archivo=archivo
        )
        messages.success(request,"La tarea fue subida correctamente")
        return redirect('detalleClase', id=tarea.clase.id) 
    return redirect('error')  

@login_required
def realizarTarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.user.es_maestro:
        return HttpResponseForbidden("Los maestros no pueden entregar tareas.")

    entrega = Entrega.objects.filter(tarea=tarea, estudiante=request.user).first()

    if request.method == "POST":
        if "eliminar" in request.POST:
            if entrega:
                entrega.delete()
                messages.success(request, "Tu entrega ha sido eliminada.")
            else:
                messages.error(request, "No tienes entrega para eliminar.")
            return redirect("realizarTarea", tarea_id=tarea.id)

        comentario = request.POST.get("comentario", "").strip()
        archivo = request.FILES.get("archivo")

        if entrega:
            entrega.comentario = comentario
            if archivo:
                entrega.archivo = archivo
            entrega.fecha_entrega = now()
            entrega.save()
            messages.success(request, "Tu entrega ha sido actualizada.")
        else:
            Entrega.objects.create(
                tarea=tarea,
                estudiante=request.user,
                comentario=comentario,
                archivo=archivo,
            )
            messages.success(request, "Tu tarea ha sido entregada.")

        return redirect("realizarTarea", tarea_id=tarea.id)

    return render(request, "realizarTarea.html", {
        "tarea": tarea,
        "entrega": entrega,
    })

@login_required
def retroalimentarEntrega(request, entrega_id):
    if not request.user.es_maestro:
        return HttpResponseForbidden("Solo los maestros pueden retroalimentar entregas.")
    entrega = get_object_or_404(Entrega, id=entrega_id)
    if request.method == "POST":
        comentario = request.POST.get("retroalimentacion", "").strip()
        if comentario:
            Retroalimentacion.objects.create(
                entrega=entrega, maestro=request.user, comentario=comentario
            )
            messages.success(request, "Retroalimentación enviada con éxito.")
        else:
            messages.error(request, "El comentario no puede estar vacío.")
        return redirect("detalleTarea", tarea_id=entrega.tarea.id)
    return render(request, "retroalimentarEntrega.html", {"entrega": entrega})


@login_required
def verRetroalimentacion(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id)
    if entrega.estudiante != request.user and not request.user.es_maestro:
        return HttpResponseForbidden("No tienes permiso para ver esta retroalimentación.")
    retroalimentaciones = entrega.retroalimentaciones.all()
    return render(request, "verRetroalimentacion.html", {"entrega": entrega, "retroalimentaciones": retroalimentaciones})

@login_required
def editarRetroalimentacion(request, retro_id):
    retroalimentacion = get_object_or_404(Retroalimentacion, id=retro_id)

    if retroalimentacion.maestro != request.user:
        messages.error(request, "No tienes permiso para editar esta retroalimentación.")
        return redirect("verRetroalimentacion", retroalimentacion.entrega.id)

    if request.method == "POST":
        comentario = request.POST.get("comentario", "").strip()
        if comentario:
            retroalimentacion.comentario = comentario
            retroalimentacion.fecha_retroalimentacion = now()
            retroalimentacion.save()
            messages.success(request, "Retroalimentación actualizada exitosamente.")
            return redirect("verRetroalimentacion", retroalimentacion.entrega.id)
        else:
            messages.error(request, "El comentario no puede estar vacío.")

    return render(request, "editarRetroalimentacion.html", {"retroalimentacion": retroalimentacion})

@login_required
def eliminarRetroalimentacion(request, retro_id):
    retroalimentacion = get_object_or_404(Retroalimentacion, id=retro_id)

    if not request.user.es_maestro or retroalimentacion.maestro != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar esta retroalimentación.")

    if request.method == "POST":
        retroalimentacion.delete()
        messages.success(request, "Retroalimentación eliminada con éxito.")
        return redirect("verRetroalimentacion", retroalimentacion.entrega.id)

    return render(request, "eliminarRetroalimentacion.html", {"retroalimentacion": retroalimentacion})

