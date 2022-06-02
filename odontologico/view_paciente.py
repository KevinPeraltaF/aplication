import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Paciente


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_paciente(request):
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
            if peticion == 'add_paciente':
                try:
                    data['titulo'] = 'Agregar nuevo paciente'
                    data['titulo_formulario'] = 'Formulario de registro de paciente'
                    data['peticion'] = 'add_paciente'
                    form = PersonaForm()
                    data['form'] = form
                    return render(request, "paciente/add_paciente.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass
        else:
            try:
                data['titulo'] = 'Pacientes'
                data['titulo_tabla'] = 'Lista  de Pacientes'
                lista = Paciente.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "paciente/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
