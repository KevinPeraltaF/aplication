from django.contrib import admin
from django.urls import path

from odontologico.conf_modulo import view_modulo
from odontologico.conf_sistema import view_conf_sistema
from odontologico.views import login_usuario, dashboard, logout_usuario

urlpatterns = [
    path(r'login/', login_usuario, name='login_usuario'),
    path(r'logout/', logout_usuario, name='logout_usuario'),
    path(r'', dashboard, name='dashboard'),
    path(r'conf_sistemas/', view_conf_sistema, name='conf_sistema'),
    path(r'conf_sistemas/modulos/', view_modulo, name='conf_modulo'),
]
