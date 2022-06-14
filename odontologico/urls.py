from django.contrib import admin
from django.urls import path

from odontologico.conf_acceso_modulo import view_acceso_modulo
from odontologico.conf_grupo import view_grupo
from odontologico.conf_modulo import view_modulo
from odontologico.conf_persona import view_persona
from odontologico.conf_usuario import view_usuario
from odontologico.view_agendar_cita import view_agendar_cita
from odontologico.view_agendar_cita_online import view_agendar_cita_online
from odontologico.view_asistente import view_asistente
from odontologico.view_atender_cita import view_atender_cita
from odontologico.view_doctor import view_doctor
from odontologico.view_paciente import view_paciente
from odontologico.view_tratamiento import view_tratamiento
from odontologico.views import login_usuario, dashboard, logout_usuario, registrate

urlpatterns = [
    path(r'', dashboard, name='dashboard'),
    path(r'login/', login_usuario, name='login_usuario'),
    path(r'registrate/', registrate, name='registrate_usuario'),
    path(r'logout/', logout_usuario, name='logout_usuario'),
    path(r'conf_sistemas/grupos/', view_grupo, name='conf_grupo'),
    path(r'conf_sistemas/modulos/', view_modulo, name='conf_modulo'),
    path(r'conf_sistemas/acceso_modulos/', view_acceso_modulo, name='conf_acceso_modulo'),
    path(r'conf_sistemas/personas/', view_persona, name='conf_persona'),
    path(r'conf_sistemas/usuarios/', view_usuario, name='conf_usuario'),
    path(r'pacientes/', view_paciente, name='pacientes'),
    path(r'doctores/', view_doctor, name='doctores'),
    path(r'asistentes/',view_asistente, name='asistentes'),
    path(r'agendar_cita/',view_agendar_cita, name='agendar_cita'),
    path(r'atender_cita/',view_atender_cita, name='atender_cita'),
    path(r'cita_online/',view_agendar_cita_online, name='agendar_cita_online'),
    path(r'tratamiento/',view_tratamiento, name='tratamiento'),
]
