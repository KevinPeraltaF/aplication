import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import ConsultaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import AgendarCita, Persona


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_atender_cita(request):
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

            if peticion == 'anular_cita':
                try:
                    with transaction.atomic():
                        registro = AgendarCita.objects.get(pk=request.POST['id'])
                        registro.estado_cita = 3
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Cita anulada correctamente."})

                except Exception as ex:
                    pass
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'atender_consulta':
                try:
                    data['titulo'] = 'Consulta'
                    data['titulo_formulario'] = 'Formulario de atención de consulta a paciente'
                    data['peticion'] = 'atender_consulta'
                    data['cita'] = AgendarCita.objects.get(pk=request.GET['id'])
                    form2 = ConsultaForm()
                    data['form2'] = form2
                    return render(request, "atender_cita/consulta.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass
        else:
            try:
                data['titulo'] = 'Citas Planificadas'
                data['titulo_tabla'] = 'Lista  de citas'
                if not persona_logeado =='SUPERADMINISTRADOR':
                    lista = AgendarCita.objects.filter(status=True,doctor__persona= persona_logeado ).order_by('-estado_cita')
                else:
                    lista = AgendarCita.objects.filter(status=True).order_by('fecha')

                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj

                return render(request, "atender_cita/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
