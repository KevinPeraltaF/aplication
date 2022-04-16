from django.contrib import admin

# Register your models here.
from odontologico.models import Modulo

@admin.register(Modulo)
class MenuAdmin(admin.ModelAdmin):
    '''Admin View for Menu'''

    list_display = ('nombre','descripcion','icono','ruta','activo','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    list_filter = ('nombre','descripcion','activo',)
    search_fields = ('nombre','descripcion',)
