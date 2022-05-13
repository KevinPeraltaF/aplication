import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from aplication import settings
from odontologico.forms import RegistroUsuarioForm
from odontologico.funciones import add_data_aplication
from odontologico.models import Modulo, Persona, Paciente


@transaction.atomic()
def login_usuario(request):
    global ex
    data = {}
    add_data_aplication(request, data)
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'login_usuario':
                try:
                    usuario = authenticate(username=request.POST['usuario'].lower().strip(),
                                           password=request.POST['clave'])
                    if usuario is not None:
                        if usuario.is_active:
                            login(request, usuario)
                            request.session['persona'] = 'persona'
                            return JsonResponse({"respuesta": True, "url": settings.LOGIN_REDIRECT_URL,
                                                 "sesion_id": request.session.session_key})
                        else:
                            return JsonResponse(
                                {"respuesta": False, 'mensaje': u'Inicio de sesión incorrecto, usuario no activo.'})
                    else:
                        return JsonResponse({"respuesta": False,
                                             'mensaje': u'Inicio de sesión incorrecto, usuario o clave no coinciden.'})
                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse(
                        {"respuesta": False, "mensaje": "Error al iniciar sesión, intentelo más tarde."})
        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
        else:
            try:
                if 'persona' in request.session:
                    return HttpResponseRedirect("/")
                data['titulo'] = 'Inicio de sesión'
                data['request'] = request
                return render(request, "registration/login.html", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))


def logout_usuario(request):
    logout(request)
    return HttpResponseRedirect("/login")

@transaction.atomic()
def registrate(request):
    global ex
    data = {}
    if request.method == 'POST':
        try:
            if request.session.get('id') != None:  # Regístrese solo cuando no haya iniciado sesión
                return JsonResponse({"respuesta": False, "mensaje": "Ya tiene sesión iniciada."})
            form = RegistroUsuarioForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                nombre1 = form.cleaned_data['nombre1']
                nombre2 = form.cleaned_data['nombre2']
                apellido1 = form.cleaned_data['apellido1']
                apellido2 = form.cleaned_data['apellido2']
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
                    email=email
                )
                persona.save()

                paciente = Paciente(
                    persona=persona
                )
                paciente.save()
                return JsonResponse({"respuesta": True, "mensaje": "A continuación ingrese con sus credenciales de acceso."})

            else:
                return render(request, "registration/registrate.html", {'form': form})
        except Exception as ex:
            transaction.set_rollback(True)
            return JsonResponse({"respuesta": False, "mensaje": "Ha ocurrido un error, intente mas tarde."})

    else:
        data['form'] = RegistroUsuarioForm()

    return render(request, "registration/registrate.html", data)


@login_required(redirect_field_name='next', login_url='/login')
@transaction.atomic()
def dashboard(request):
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
            if peticion == 'peticion':
                try:
                    pass
                except Exception as ex:
                    transaction.set_rollback(True)
                    pass
        else:
            try:
                data['titulo'] = 'Menú principal'
                data['modulos'] = modulos = Modulo.objects.filter(status=True, activo=True)
                return render(request, "registration/dashboard.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
