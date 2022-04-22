import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
                        return JsonResponse({"respuesta": True, "mensaje": "Registro guardado correctamente."})

                    else:
                        return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})

                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})
            if peticion == 'eliminar_modulo':
                try:
                    with transaction.atomic():
                        registro = Modulo.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save()
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass

        return JsonResponse({"respuesta": False, "mensaje": "No se ha encontrado respuesta."})
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
                lista_modulos = Modulo.objects.filter(status=True)
                paginator = Paginator(lista_modulos, 1)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "conf_sistema/view_modulo.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
