import sys
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.funciones import add_data_aplication
from odontologico.models import Modulo


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_conf_sistema(request):
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
                     'descripcion': 'Configuración y administración de grupos del sistemas',
                     'icono': '/media/icono/grupos.png',
                     'ruta': 'conf_sistemas/grupos/'
                     },
                    {'nombre': 'Modulos',
                     'descripcion': 'Configuración y administración de modulos del sistema',
                     'icono': '/media/icono/modulos.png',
                     'ruta': 'conf_sistemas/modulos/'
                     },
                    {'nombre': 'Personas',
                     'descripcion': 'Configuración y administración de personas del sistemas',
                     'icono': '/media/icono/personas.png',
                     'ruta': 'conf_sistemas/personas/'
                     },
                    {'nombre': 'Usuarios',
                     'descripcion': 'Configuración y administración de usuarios del sistema',
                     'icono': '/media/icono/usuarios.png',
                     'ruta': 'conf_sistemas/usuarios/'
                     }

                ]
                data['modulos'] = modulos_administracion_sistema
                return render(request, "conf_sistema/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
