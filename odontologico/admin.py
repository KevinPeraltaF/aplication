from django.contrib import admin

# Register your models here.
from odontologico.models import Modulo,Genero,Persona,Paciente

@admin.register(Modulo)
class MenuAdmin(admin.ModelAdmin):
    '''Admin View for Menu'''

    list_display = ('nombre','descripcion','icono','ruta','activo','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    list_filter = ('nombre','descripcion','activo',)
    search_fields = ('nombre','descripcion',)


@admin.register(Genero)
class MenuAdmin(admin.ModelAdmin):
    '''Admin View for Genero'''

    list_display = ('nombre','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Persona)
class MenuAdmin(admin.ModelAdmin):
    '''Admin View for Persona'''

    list_display = ('usuario','nombre1','nombre2','apellido1','apellido2','email','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    search_fields = ('apellido1','apellido2','email',)

@admin.register(Paciente)
class MenuAdmin(admin.ModelAdmin):
    '''Admin View for Paciente'''

    list_display = ('persona','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion','status',)
    list_filter = ('persona',)
    search_fields = ('persona',)