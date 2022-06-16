import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Paciente, PersonaPerfil, Persona


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_paciente(request):
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

            if peticion == 'add_paciente':
                try:
                    form = PersonaForm(request.POST, request.FILES)
                    if form.is_valid():

                        campos_repetidos = list()

                        if Persona.objects.values('id').filter(cedula=form.cleaned_data['cedula'], status=True).exists():
                            campos_repetidos.append(form['cedula'].name)
                        if Persona.objects.values('id').filter(email=form.cleaned_data['email'], status=True).exists():
                            campos_repetidos.append(form['email'].name)
                        if campos_repetidos:
                            return JsonResponse(
                                {"respuesta": False, "mensaje": "registro ya existe.", 'repetidos': campos_repetidos})

                        username = form.cleaned_data['cedula']
                        password = form.cleaned_data['cedula']
                        nombre1 = form.cleaned_data['nombre1']
                        nombre2 = form.cleaned_data['nombre2']
                        apellido1 = form.cleaned_data['apellido1']
                        apellido2 = form.cleaned_data['apellido2']
                        cedula = form.cleaned_data['cedula']
                        genero = form.cleaned_data['genero']
                        telefono_movil = form.cleaned_data['telefono_movil']
                        telefono_convencional = form.cleaned_data['telefono_convencional']
                        email = form.cleaned_data['email']
                        username = username.strip()  # Eliminar espacios y líneas nuevas
                        password = password.strip()
                        usuario = User.objects.create_user(username, '', password)
                        usuario.save()

                        grupo = Group.objects.get(pk=4)  # PACIENTE
                        grupo.user_set.add(usuario)

                        persona = Persona(
                            usuario=usuario,
                            nombre1=nombre1,
                            nombre2=nombre2,
                            apellido1=apellido1,
                            apellido2=apellido2,
                            email=email,
                            cedula=cedula,
                            genero=genero,
                            telefono_movil=telefono_movil,
                            telefono_convencional=telefono_convencional
                        )
                        persona.save(request)

                        persona_perfil = PersonaPerfil(
                            persona=persona,
                            is_paciente=True
                        )

                        persona_perfil.save(request)

                        paciente = Paciente(
                            persona=persona
                        )
                        paciente.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro guardado correctamente."})
                    else:
                       return JsonResponse(  {"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})


                except Exception as ex:
                   transaction.set_rollback(True)
                   return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'edit_paciente':
                try:
                    form = PersonaForm(request.POST, request.FILES)
                    if form.is_valid():
                        paciente = Paciente.objects.get(pk=request.POST['id'])
                        persona = Persona.objects.get(pk = paciente.persona_id)
                        persona.nombre1 =request.POST['nombre1']
                        persona.nombre2 =request.POST['nombre2']
                        persona.apellido1=request.POST['apellido1']
                        persona.apellido2=request.POST['apellido2']
                        persona.email=request.POST['email']
                        persona.cedula=request.POST['cedula']
                        persona.genero_id=request.POST['genero']
                        persona.telefono_movil=request.POST['telefono_movil']
                        persona.telefono_convencional=request.POST['telefono_convencional']
                        persona.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro Modificado correctamente."})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'eliminar_paciente':
                try:
                    with transaction.atomic():
                        registro = Paciente.objects.get(pk=request.POST['id'])
                        registro.status = False
                        registro.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro eliminado correctamente."})

                except Exception as ex:
                    pass
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

            if peticion == 'historial_odontograma':
                try:
                    data['titulo'] = 'Historial - Odontogramas'
                    data['titulo_formulario'] = 'Odontograma'
                    data['peticion'] = 'historial_odontograma'

                    return render(request, "paciente/historial_odontograma.html", data)
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass

            if peticion == 'edit_paciente':
                try:
                    data['titulo'] = 'Editar paciente'
                    data['titulo_formulario'] = 'Formulario de editar paciente'
                    data['peticion'] = 'edit_paciente'
                    data['paciente'] = paciente = Paciente.objects.get(pk=request.GET['id'])
                    form = PersonaForm(initial={
                        'nombre1':paciente.persona.nombre1,
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
                data['titulo'] = 'Pacientes'
                data['titulo_tabla'] = 'Lista  de Pacientes'
                data['persona_logeado'] = persona_logeado
                lista = Paciente.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "paciente/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
