import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Persona, Doctor


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_reportes(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    usuario_logeado = request.user
    if Persona.objects.filter(usuario=usuario_logeado, status=True).exists():
        persona_logeado = Persona.objects.get(usuario=usuario_logeado, status=True)
    else:
        persona_logeado = 'SUPERADMINISTRADOR'

    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'eliminar_doctor':
                try:
                    with transaction.atomic():
                        registro = Doctor.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'add_doctor':
                try:
                    data['titulo'] = 'Agregar nuevo doctor'
                    data['titulo_formulario'] = 'Formulario de registro de doctor'
                    data['peticion'] = 'add_doctor'
                    form = PersonaForm()
                    data['form'] = form
                    return render(request, "doctor/add_doctor.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass


        else:
            try:
                data['titulo'] = 'Reportes'
                data['persona_logeado'] = persona_logeado

                return render(request, "reportes/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))