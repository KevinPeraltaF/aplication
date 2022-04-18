from django.contrib import admin
from django.urls import path

from odontologico.conf_grupo import view_grupo
from odontologico.conf_modulo import view_modulo
from odontologico.conf_persona import view_persona
from odontologico.conf_usuario import view_usuario
from odontologico.views import login_usuario, dashboard, logout_usuario

urlpatterns = [
    path(r'', dashboard, name='dashboard'),
    path(r'login/', login_usuario, name='login_usuario'),
    path(r'logout/', logout_usuario, name='logout_usuario'),
    path(r'conf_sistemas/grupos/', view_grupo, name='conf_modulo'),
    path(r'conf_sistemas/modulos/', view_modulo, name='conf_modulo'),
    path(r'conf_sistemas/personas/', view_persona, name='conf_modulo'),
    path(r'conf_sistemas/usuarios/', view_usuario, name='conf_modulo'),
]
