from django.db import models
from odontologico.funciones import ModeloBase

class Modulo(ModeloBase):
    nombre = models.CharField(verbose_name="Nombre del módulo",max_length=100,unique=True)
    descripcion= models.CharField(verbose_name="Descripción", default='',max_length=200)
    icono = models.ImageField(verbose_name="Icono", upload_to='icono/')
    ruta = models.CharField(default='', max_length=200, verbose_name='Ruta')
    activo = models.BooleanField(verbose_name="¿Módulo activo?",default=True)
    modulo_padre = models.ForeignKey('self',verbose_name="Módulo Padre", null=True, blank=True, on_delete=models.CASCADE)
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
        return super(Modulo, self).save(*args, **kwargs)

    def tiene_submodulo(self):
        existe = Modulo.objects.filter(status=True,activo=True,modulo_padre=self.pk).exists()
        return existe

