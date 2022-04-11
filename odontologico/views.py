from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
@transaction.atomic()
def login_usuario(request):
    global ex
    data = {}
    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']
            if peticion == 'login_usuario':
                try:
                    return JsonResponse({"respuesta": True}, safe=False)
                except Exception as ex:
                    transaction.set_rollback(True)
                    return JsonResponse({"respuesta": False, "mensaje": "Error al iniciar sesión, intentelo más tarde."})

        return JsonResponse({"respuesta": False, "mensaje": "acción Incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']
        else:
            pass
    return render(request, "registration/login.html", data)
