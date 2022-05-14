from django.contrib.auth.models import User
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
        ordering = ['nombre']
        unique_together = ('ruta',)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip().capitalize()
        self.descripcion = self.descripcion.strip().capitalize()
        self.ruta = self.ruta.strip().capitalize()
        return super(Modulo, self).save(*args, **kwargs)


class Genero(ModeloBase):
    nombre = models.CharField(max_length=100, verbose_name=u'Género')


class Persona(ModeloBase):
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    nombre1 = models.CharField(max_length=100, verbose_name=u'1er Nombre')
    nombre2 = models.CharField(max_length=100, verbose_name=u'2do Nombre')
    apellido1 = models.CharField(max_length=100, verbose_name=u"1er Apellido")
    apellido2 = models.CharField(max_length=100, verbose_name=u"2do Apellido")
    email = models.CharField(default='', max_length=200, verbose_name=u"Correo electronico personal", unique=True)
    cedula = models.CharField( max_length=10, verbose_name=u'Cédula', unique=True)
    telefono_movil = models.CharField(max_length=12, verbose_name=u"Teléfono móvil")
    telefono_convencional = models.CharField(max_length=10, verbose_name=u"Teléfono móvil", null=True, blank=True)
    genero = models.ForeignKey(Genero, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return u'%s %s %s %s' % (self.apellido1, self.apellido2, self.nombre1, self.nombre1)


class Paciente(ModeloBase):
    persona = models.ForeignKey(Persona, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s' % self.persona
