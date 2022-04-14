from django.contrib import admin
from django.urls import path

from odontologico.views import login_usuario, dashboard

urlpatterns = [
    path(r'login/', login_usuario, name='login_usuario'),
    path(r'', dashboard, name='dashboard'),
]
