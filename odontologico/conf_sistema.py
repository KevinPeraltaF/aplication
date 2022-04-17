import sys
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.funciones import add_data_aplication
from odontologico.models import Modulo


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'peticion':
                try:
                    pass
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass
        else:
            try:
                data['titulo'] = 'Configuración del sistema'
                modulos_administracion_sistema = [
                    {'nombre': 'Grupos',
                     'descripcion': 'Configuración y administración de grupos de sistemas',
                     'icono': '/media/icono/groups_people_people_1715.png',
                     'ruta': 'conf_grupos/'},
                    {'nombre': 'Personas',
                     'descripcion': 'Configuración y administración de grupos de sistemas',
                     'icono': '/media/icono/persona.png',
                     'ruta': 'conf_grupos/'},
                    {'nombre': 'Usuarios',
                     'descripcion': 'Configuración y administración de usuarios del sistema',
                     'icono': '/media/icono/rotation_102346.png',
                     'ruta': 'conf_usuarios/'}

                ]
                data['modulos'] =modulos_administracion_sistema
                return render(request, "conf_sistema/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
