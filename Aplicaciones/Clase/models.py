from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    es_maestro = models.BooleanField(default=False)

# Modelo para Clases
class Clase(models.Model):
    id = models.AutoField(primary_key=True) 
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    maestro = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'es_maestro': True}, related_name="clases")
    video_url = models.URLField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# Modelo para Materiales
class Material(models.Model):
    id = models.AutoField(primary_key=True) 
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="materiales")
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to="materiales/")

    def __str__(self):
        return self.titulo
# Modelo para Tareas
class Tarea(models.Model):
    id = models.AutoField(primary_key=True) 
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="tareas")
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()

    def __str__(self):
        return self.titulo

# Modelo para Entregas de Tareas
class Entrega(models.Model):
    id = models.AutoField(primary_key=True) 
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="entregas")
    estudiante = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'es_maestro': False}, related_name="entregas")
    archivo = models.FileField(upload_to="entregas/")
    comentario = models.TextField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrega de {self.estudiante.username} para {self.tarea.titulo}"

# Modelo para Retroalimentaciones
class Retroalimentacion(models.Model):
    id = models.AutoField(primary_key=True) 
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name="retroalimentaciones")
    maestro = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'es_maestro': True}, related_name="retroalimentaciones")
    comentario = models.TextField()
    fecha_retroalimentacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Retroalimentación de {self.maestro.username} para {self.entrega.estudiante.username}"
