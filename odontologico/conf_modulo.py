import sys
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from odontologico.funciones import add_data_aplication
from odontologico.models import Modulo


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_modulo(request):
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
            if peticion == 'add_modulo':
                try:
                    data['titulo'] = 'Agregar nuevo módulo'
                    data['titulo_formulario'] = 'Formulario de registro de Módulo'
                    return render(request, "conf_sistema/add_modulo.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass
        else:
            try:
                data['titulo'] = 'Configuración de Módulos'
                data['titulo_tabla'] = 'Lista  de Módulos'
                modulos = Modulo.objects.filter(status=True)
                data['modulos'] = modulos
                return render(request, "conf_sistema/view_modulo.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
