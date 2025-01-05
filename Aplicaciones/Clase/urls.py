from django.urls import path
from . import views
urlpatterns=[
    path('',views.inicio, name='inicio'),
    path('logout/', views.signout, name='logout'),
    path('dashboard_maestro/', views.dashboard_maestro, name='dashboard_maestro'),
    path('dashboard_estudiante/', views.dashboard_estudiante, name='dashboard_estudiante'),
    #Clase
    path('nuevaClase/', views.nuevaClase, name='nuevaClase'),
    path('listadoClase/',views.listadoClase, name='listadoClase'),
    path('detalleClase/<int:id>/', views.detalleClase, name='detalleClase'),  # Para ver detalles de una clase
    path('guardarClase/', views.guardarClase, name='guardarClase'),
    path('eliminarClase/<id>/',views.eliminarClase, name='eliminarClase'),
    path('editarClase/<id>/',views.editarClase, name='editarClase'),
    path('procesarEdicionClase/', views.procesarEdicionClase, name='procesarEdicionClase'),
    #Material
    path('clases/<int:clase_id>/nuevoMaterial/', views.nuevoMaterial, name='nuevoMaterial'),
    path('clases/<int:clase_id>/materiales/', views.verMaterial, name='verMaterial'),
    
    path('material/<int:material_id>/editar/', views.editarMaterial, name='editarMaterial'),
    path('material/<int:material_id>/eliminar/', views.eliminarMaterial, name='eliminarMaterial'),
    path('material/<int:material_id>/detalle/',views.detalleMaterial, name='detalleMaterial'),

    #Tarea
    path('clases/<int:clase_id>/nuevaTarea/', views.nuevaTarea, name='nuevaTarea'),
    path('clases/<int:clase_id>/tareas/', views.listaTareas, name='listaTareas'),
    path('clases/<int:clase_id>/tareas/', views.verTareas, name='verTareas'),
    path('tareas/<int:tarea_id>/subir/', views.subirTarea, name='subirTarea'),
    path('tareas/<int:tarea_id>/editar/', views.editarTarea, name='editarTarea'),
    path('tareas/<int:tarea_id>/eliminar/', views.eliminarTarea, name='eliminarTarea'),
    #Entregas  
    path('tareas/<int:tarea_id>/realizar/', views.realizarTarea, name='realizarTarea'),
    path('tareas/<int:tarea_id>/detalle/', views.detalleTarea, name='detalleTarea'),

    #Retroalimentacion
    path('retroalimentar/<int:entrega_id>/', views.retroalimentarEntrega, name='retroalimentarEntrega'),
    path('verRetroalimentacion/<int:entrega_id>/', views.verRetroalimentacion, name='verRetroalimentacion'),
    path('retroalimentacion/<int:retro_id>/editar/', views.editarRetroalimentacion, name='editarRetroalimentacion'),
    path('retroalimentacion/<int:retro_id>/eliminar/', views.eliminarRetroalimentacion, name='eliminarRetroalimentacion')
]
    