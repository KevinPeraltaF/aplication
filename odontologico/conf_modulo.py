import sys
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from odontologico.forms import ModuloForm
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
            if peticion == 'add_modulo':
                try:
                    form = ModuloForm(request.POST, request.FILES)
                    if form.is_valid():
                        modulo = Modulo(
                            nombre=form.cleaned_data['nombre'],
                            descripcion=form.cleaned_data['descripcion'],
                            icono=form.cleaned_data['icono'],
                            ruta=form.cleaned_data['ruta'],
                            activo=form.cleaned_data['activo']
                        )
                        modulo.save()
                        return JsonResponse({"respuesta": True, "mensaje": "Datos guardados correctamente."})

                    else:
                        return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})

                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

        return JsonResponse({"respuesta": False, "mensaje": "No se ha encontrado respuesta.."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
            if peticion == 'add_modulo':
                try:
                    data['titulo'] = 'Agregar nuevo módulo'
                    data['titulo_formulario'] = 'Formulario de registro de Módulo'
                    data['peticion'] = 'add_modulo'
                    data['form'] = ModuloForm()
                    return render(request, "conf_sistema/add_modulo.html", data)
                except Exception as ex:
                    pass
        else:
            try:
                data['titulo'] = 'Configuración de Módulos'
                data['titulo_tabla'] = 'Lista  de Módulos'
                data['modulos'] = modulos = Modulo.objects.filter(status=True)
                return render(request, "conf_sistema/view_modulo.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
