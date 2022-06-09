import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm, AgendarCitaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import PersonaPerfil, Persona, Asistente, AgendarCita


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_agendar_cita(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']

            if peticion == 'eliminar_cita':
                try:
                    with transaction.atomic():
                        registro = AgendarCita.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

            if peticion == 'add_cita':
                try:
                    data['titulo'] = 'Agendar nueva cita'
                    data['titulo_formulario'] = 'Formulario de registro de citas'
                    data['peticion'] = 'add_cita'
                    form = AgendarCitaForm()
                    data['form'] = form
                    return render(request, "agendar_cita/add_cita.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'edit_cita':
                try:
                    data['titulo'] = 'Editar cita'
                    data['titulo_formulario'] = 'Formulario de editar paciente'
                    data['peticion'] = 'edit_paciente'
                    data['paciente'] = paciente = Paciente.objects.get(pk=request.GET['id'])
                    form = PersonaForm(initial={
                        'nombre1': paciente.persona.nombre1,
                        'nombre2': paciente.persona.nombre2,
                        'apellido1': paciente.persona.apellido1,
                        'apellido2': paciente.persona.apellido2,
                        'email': paciente.persona.email,
                        'cedula': paciente.persona.cedula,
                        'genero': paciente.persona.genero,
                        'telefono_movil': paciente.persona.telefono_movil,
                        'telefono_convencional': paciente.persona.telefono_convencional
                    })
                    form.editar()
                    data['form'] = form
                    return render(request, "paciente/edit_paciente.html", data)
                except Exception as ex:
                    pass

        else:
            try:
                data['titulo'] = 'Agendar Cita'
                data['titulo_tabla'] = 'Lista  de citas'
                lista = AgendarCita.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "agendar_cita/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
