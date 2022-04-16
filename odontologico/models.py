from django.db import models
from odontologico.funciones import ModeloBase

class Modulo(ModeloBase):
    nombre = models.CharField(verbose_name="Nombre del módulo",max_length=100,unique=True)
    descripcion= models.CharField(verbose_name="Descripción", default='',null=True,blank=True,max_length=200)
    icono = models.ImageField(verbose_name="Icono", blank=True, null=True, upload_to='icono/')
    ruta = models.CharField(default='', max_length=200, verbose_name='Ruta')
    activo = models.BooleanField(verbose_name="¿Módulo activo?",default=True)

    class Meta:
        verbose_name="Módulo del sistema"
        verbose_name_plural = "Módulos del sistema"
        ordering = ['nombre']
        unique_together = ('ruta',)
    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self, *args, **kwargs):
        self.nombre= self.nombre.strip()
        self.descripcion = self.descripcion.strip()
        self.ruta = self.ruta.strip()
        self.icono=self.icono.strip()
        return super(Modulo, self).save(*args, **kwargs)



