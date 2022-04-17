import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from aplication import settings
from odontologico.funciones import add_data_aplication
from odontologico.models import Modulo


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
                                {"result": False, 'mensaje': u'Inicio de sesión incorrecto, usuario no activo.'})
                    else:
                        return JsonResponse(
                            {"result": False, 'mensaje': u'Inicio de sesión incorrecto, usuario incorrecto.'})
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
                data['modulos'] = modulos = Modulo.objects.filter(status=True ,activo=True, modulo_padre__isnull=True)
                return render(request, "registration/dashboard.html ", data)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
