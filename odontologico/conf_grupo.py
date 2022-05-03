import json
import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from odontologico.funciones import add_data_aplication


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_grupo(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'eliminar_grupo':
                try:
                    with transaction.atomic():
                        registro = Group.objects.get(pk=request.POST['id'])
                        registro.delete()
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass
            if peticion == 'add_grupo':
                try:
                    items = json.loads(request.POST['items'])

                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "No se ha encontrado respuesta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'add_grupo':
                try:
                    data['titulo'] = 'Agregar nuevo grupo'
                    data['titulo_formulario'] = 'Formulario de registro de grupos'
                    data['peticion'] = 'add_grupo'
                    data['permisos'] =Permission.objects.all()

                    return render(request, "conf_sistema/add_grupo.html", data)
                except Exception as ex:
                    pass
        else:
            try:
                data['titulo'] = 'Configuración de grupos'
                data['titulo_tabla'] = 'Lista  de Grupos'
                lista = Group.objects.all().order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj

                return render(request, "conf_sistema/view_grupo.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
