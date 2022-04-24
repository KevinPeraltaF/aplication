import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
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
            if 'peticion' in request.GET:
                peticion = request.GET['peticion']
                if peticion == 'add_modulo':
                    try:
                        data['titulo'] = 'Agregar nuevo grupo'
                        data['titulo_formulario'] = 'Formulario de registro de grupos'
                        data['peticion'] = 'edit_grupo'

                        return render(request, "conf_sistema/add_grupo.html", data)
                    except Exception as ex:
                        pass

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
