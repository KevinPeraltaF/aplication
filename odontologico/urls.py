from django.contrib import admin
from django.urls import path

from odontologico.views import login_usuario

urlpatterns = [
    path(r'login/',login_usuario, name='login_usuario'),
]