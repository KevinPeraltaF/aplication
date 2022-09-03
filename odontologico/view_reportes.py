import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Persona, Doctor, Paciente, Tratamiento, Consulta, Asistente


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
            if peticion == 'reporte_pacientes':
                try:
                    fila = Paciente.objects.filter(status=True)
                except Exception as ex:
                    pass

            if peticion == 'reporte_asistentes':
                try:
                    fila = Asistente.objects.filter(status=True)
                except Exception as ex:
                    pass

            if peticion == 'reporte_especialistas':
                try:
                    fila = Doctor.objects.filter(status=True)
                except Exception as ex:
                    pass

            if peticion == 'reporte_tratamiento':
                try:
                    fila = Tratamiento.objects.filter(status=True)
                except Exception as ex:
                    pass

            if peticion == 'reporte_tratamiento_por_paciente':
                try:
                    fila = Consulta.objects.raw(
                        'SELECT trat.id, trat.nombre, ( SELECT  COUNT(c.consulta_id) AS paciente FROM odontologico_consulta_tratamientos c WHERE c.tratamiento_id=trat.id group by c.tratamiento_id ) AS cantidad_pacientes FROM  odontologico_tratamiento trat ')

                except Exception as ex:
                    pass


        else:
            try:
                data['titulo'] = 'Reportes'
                data['persona_logeado'] = persona_logeado
                data['pacientes_masculino']  = pacientes_masculino = Paciente.objects.filter(status=True, persona__genero__pk = 1).count()
                data['pacientes_femenino'] =pacientes_femenino = Paciente.objects.filter(status=True, persona__genero__pk = 2).count()

                #pacientes por tratamientos
                data['tratamientos'] = tratamientos = Tratamiento.objects.filter(status = True)
                data['consultas'] =consultas = Consulta.objects.raw('SELECT trat.id, trat.nombre, ( SELECT  COUNT(c.consulta_id) AS paciente FROM odontologico_consulta_tratamientos c WHERE c.tratamiento_id=trat.id group by c.tratamiento_id ) AS cantidad_pacientes FROM  odontologico_tratamiento trat ')
                tratamientos = []
                cantidad_pacientes = []
                for c in consultas:

                    tratamientos.append(c.nombre)
                    if c.cantidad_pacientes is None:
                        valor = 0
                    else:
                        valor =c.cantidad_pacientes
                    cantidad_pacientes.append(valor)
                data['tratamientos'] =tratamientos
                data['cantidad_pacientes'] =cantidad_pacientes
                return render(request, "reportes/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
