from django.contrib.auth.models import User, Group
from django.db import models
from odontologico.funciones import ModeloBase


class Modulo(ModeloBase):
    nombre = models.CharField(verbose_name="Nombre del módulo", max_length=100, unique=True)
    descripcion = models.CharField(verbose_name="Descripción", default='', max_length=200)
    icono = models.ImageField(verbose_name="Icono", upload_to='icono/')
    ruta = models.CharField(default='', max_length=200, unique=True, verbose_name='Ruta')
    activo = models.BooleanField(verbose_name="¿Módulo activo?")

    class Meta:
        verbose_name = "Módulo del sistema"
        verbose_name_plural = "Módulos del sistema"
        ordering = ['id']
        unique_together = ('ruta',)

    def __str__(self):
        return u'%s' % self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().capitalize()
        self.descripcion = self.descripcion.strip().capitalize()
        return super(Modulo, self).save(*args, **kwargs)


class Genero(ModeloBase):
    nombre = models.CharField(max_length=100, verbose_name=u'Género')

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ['id']

    def __str__(self):
        return u'%s' % self.nombre


class Persona(ModeloBase):
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    nombre1 = models.CharField(max_length=100, verbose_name=u'1er Nombre')
    nombre2 = models.CharField(max_length=100, verbose_name=u'2do Nombre')
    apellido1 = models.CharField(max_length=100, verbose_name=u"1er Apellido")
    apellido2 = models.CharField(max_length=100, verbose_name=u"2do Apellido")
    email = models.CharField(default='', max_length=200, verbose_name=u"Correo electronico personal", unique=True)
    cedula = models.CharField( max_length=10, verbose_name=u'Cédula', unique=True)
    telefono_movil = models.CharField(max_length=10, verbose_name=u"Teléfono móvil")
    telefono_convencional = models.CharField(max_length=10, verbose_name=u"Teléfono convencional", null=True, blank=True)
    genero = models.ForeignKey(Genero, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['id']

    def __str__(self):
        return u'%s %s %s %s' % (self.apellido1, self.apellido2, self.nombre1, self.nombre1)


    def tiene_perfil_persona(self):
        return self.personaperfil_set().exists()

class PersonaPerfil(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    is_paciente = models.BooleanField(default=False, verbose_name=u'Es paciente')
    is_administrador = models.BooleanField(default=False, verbose_name=u'Es administrador')
    is_especialista = models.BooleanField(default=False, verbose_name=u'Es especialista')
    is_asistente = models.BooleanField(default=False, verbose_name=u'Es asistente')

    class Meta:
        verbose_name = "Perfil de persona"
        verbose_name_plural = "Perfiles de personas"
        ordering = ['id']

    def __str__(self):
        if self.es_paciente():
            return u'%s' % "PACIENTE"
        elif self.es_administrador():
            return u'%s' % "ADMINISTRADOR"
        elif self.es_especialista():
            return u'%s' % "ESPECIALISTA"
        elif self.es_asistente():
            return u'%s' % "ASISTENTE"
        else:
            return u'%s' % "NO TIENE PERFIL"

    def es_paciente(self):
        return self.es_paciente

    def es_administrador(self):
        return self.es_administrador

    def es_especialista(self):
        return self.es_especialista

    def es_asistente(self):
        return self.es_asistente

class Paciente(ModeloBase):
    persona = models.ForeignKey(Persona, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['id']

    def __str__(self):
        return u'%s' % self.persona


class AccesoModulo(ModeloBase):
    grupo = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, null=True, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Acceso a módulo"
        verbose_name_plural = "Acceso a módulos"
        ordering = ['id']

    def __str__(self):
        return u'%s - %s - %s' % (self.grupo,self.modulo, self.activo)

