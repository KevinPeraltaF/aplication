from django.contrib import admin
from django.urls import path

from odontologico.conf_sistema import view
from odontologico.views import login_usuario, dashboard, logout_usuario

urlpatterns = [
    path(r'login/', login_usuario, name='login_usuario'),
    path(r'logout/', logout_usuario, name='logout_usuario'),
    path(r'', dashboard, name='dashboard'),
    path(r'conf_sistemas/', view, name='conf_sistema'),
]
