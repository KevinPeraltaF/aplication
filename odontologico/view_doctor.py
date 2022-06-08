import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from odontologico.forms import PersonaForm
from odontologico.funciones import add_data_aplication
from odontologico.models import  PersonaPerfil, Persona, Doctor


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def view_doctor(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']

            if peticion == 'add_doctor':
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
                            is_especialista=True
                        )
                        persona_perfil.save(request)

                        doctor = Doctor(
                            persona=persona
                        )
                        doctor.save(request)
                        return JsonResponse({"respuesta": True, "mensaje": "Registro guardado correctamente."})
                    else:
                       return JsonResponse(  {"respuesta": False, "mensaje": "Ha ocurrido un error al enviar los datos."})


                except Exception as ex:
                   transaction.set_rollback(True)
                   return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

            if peticion == 'edit_doctor':
                try:
                    form = PersonaForm(request.POST, request.FILES)
                    if form.is_valid():
                        doctor = Doctor.objects.get(pk=request.POST['id'])
                        persona = Persona.objects.get(pk = doctor.id)
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
                    else:
                        return render(request, "registration/registrate.html", {'form': form})


                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

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

            if peticion == 'edit_doctor':
                try:
                    data['titulo'] = 'Editar doctor'
                    data['titulo_formulario'] = 'Formulario de editar doctor'
                    data['peticion'] = 'edit_doctor'
                    data['doctor'] = doctor = Doctor.objects.get(pk=request.GET['id'])
                    form = PersonaForm(initial={
                        'nombre1':doctor.persona.nombre1,
                        'nombre2': doctor.persona.nombre2,
                        'apellido1': doctor.persona.apellido1,
                        'apellido2': doctor.persona.apellido2,
                        'email': doctor.persona.email,
                        'cedula': doctor.persona.cedula,
                        'genero': doctor.persona.genero,
                        'telefono_movil': doctor.persona.telefono_movil,
                        'telefono_convencional': doctor.persona.telefono_convencional
                    })
                    form.editar()
                    data['form'] = form
                    return render(request, "doctor/edit_doctor.html", data)
                except Exception as ex:
                    pass

        else:
            try:
                data['titulo'] = 'Doctores'
                data['titulo_tabla'] = 'Lista  de Doctores'
                lista = Doctor.objects.filter(status=True).order_by('id')
                paginator = Paginator(lista, 15)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                data['page_obj'] = page_obj
                return render(request, "doctor/view.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
