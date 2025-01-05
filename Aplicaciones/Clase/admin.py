from django.contrib import admin

from.models import CustomUser
from.models import Clase
from.models import Material
from.models import Tarea
from.models import Entrega
from.models import Retroalimentacion


# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Clase)
admin.site.register(Material)
admin.site.register(Tarea)
admin.site.register(Entrega)
admin.site.register(Retroalimentacion)