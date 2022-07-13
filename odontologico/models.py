from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Sum

from odontologico.funciones import ModeloBase

ESTADO_CITA = (
    (1, u"ATENDIDO"),
    (2, u"PENDIENTE"),
    (3, u"ANULADO"),
)

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
    email = models.CharField(default='', max_length=200, verbose_name=u"Correo electronico personal")
    cedula = models.CharField( max_length=10, verbose_name=u'Cédula')
    telefono_movil = models.CharField(max_length=10, verbose_name=u"Teléfono móvil")
    telefono_convencional = models.CharField(max_length=10, verbose_name=u"Teléfono convencional", null=True, blank=True)
    genero = models.ForeignKey(Genero, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['id']

    def __str__(self):
        return u'%s %s %s %s' % (self.apellido1, self.apellido2, self.nombre1, self.nombre2)


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
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['id']

    def __str__(self):
        return u'%s' % self.persona

    def tiene_odontograma(self):
        return self.agendarcita_set.filter(status=True, estado_cita=1).exists()

    def en_uso(self):
        existe = self.agendarcita_set.exists() | self.consulta_set.exists()
        return existe





class Doctor(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctores"
        ordering = ['id']

    def __str__(self):
        return u'%s' % self.persona

    def en_uso(self):
        existe = self.agendarcita_set.exists() | self.consulta_set.exists()
        return existe

class Asistente(ModeloBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Asistente"
        verbose_name_plural = "Asistentes"
        ordering = ['id']

    def __str__(self):
        return u'%s' % self.persona


class AccesoModulo(ModeloBase):
    grupo = models.ForeignKey(Group,  on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Acceso a módulo"
        verbose_name_plural = "Acceso a módulos"
        ordering = ['id']

    def __str__(self):
        return u'%s - %s - %s' % (self.grupo,self.modulo, self.activo)

class Horario_hora(ModeloBase):
    hora_inicio = models.TimeField(verbose_name=u"Hora inicio")
    hora_fin = models.TimeField(verbose_name=u"Hora fin")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Horario Horas de atención"
        verbose_name_plural = "Horarios Horas de atenciones"
        ordering = ['id']

    def __str__(self):
        return u'%s - %s' % (self.hora_inicio, self.hora_fin)

class AgendarCita(ModeloBase):
    paciente = models.ForeignKey(Paciente,  on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,  on_delete=models.CASCADE)
    fecha = models.DateField(verbose_name=u'Fecha')
    horario = models.ForeignKey(Horario_hora,  on_delete=models.CASCADE)
    estado_cita = models.IntegerField(choices=ESTADO_CITA, null=True, blank=True, verbose_name=u'Estado cita')

    class Meta:
        verbose_name = "Agendar cita"
        verbose_name_plural = "Agendar citas"
        ordering = ['id']

    def __str__(self):
        return u'Paciente: %s - Especialista: %s - Fecha: %s - Horario: %s' % (self.paciente,self.doctor, self.fecha,self.horario)

class Odontograma(models.Model):
    TP18=models.CharField(max_length=50, null=True)
    BP18=models.CharField(max_length=50, null=True)
    RP18=models.CharField(max_length=50, null=True)
    LP18=models.CharField(max_length=50, null=True)
    CP18=models.CharField(max_length=50, null=True)
    CP17=models.CharField(max_length=50, null=True)
    TP17=models.CharField(max_length=50, null=True)
    BP17=models.CharField(max_length=50, null=True)
    RP17=models.CharField(max_length=50, null=True)
    LP17=models.CharField(max_length=50, null=True)
    CP16=models.CharField(max_length=50, null=True)
    TP16=models.CharField(max_length=50, null=True)
    BP16=models.CharField(max_length=50, null=True)
    RP16=models.CharField(max_length=50, null=True)
    LP16=models.CharField(max_length=50, null=True)
    CP15=models.CharField(max_length=50, null=True)
    TP15=models.CharField(max_length=50, null=True)
    BP15=models.CharField(max_length=50, null=True)
    RP15=models.CharField(max_length=50, null=True)
    LP15=models.CharField(max_length=50, null=True)
    CP14=models.CharField(max_length=50, null=True)
    TP14=models.CharField(max_length=50, null=True)
    BP14=models.CharField(max_length=50, null=True)
    RP14=models.CharField(max_length=50, null=True)
    LP14=models.CharField(max_length=50, null=True)
    CP13=models.CharField(max_length=50, null=True)
    TP13=models.CharField(max_length=50, null=True)
    BP13=models.CharField(max_length=50, null=True)
    RP13=models.CharField(max_length=50, null=True)
    LP13=models.CharField(max_length=50, null=True)
    CP12=models.CharField(max_length=50, null=True)
    TP12=models.CharField(max_length=50, null=True)
    BP12=models.CharField(max_length=50, null=True)
    RP12=models.CharField(max_length=50, null=True)
    LP12=models.CharField(max_length=50, null=True)
    CP11=models.CharField(max_length=50, null=True)
    TP11=models.CharField(max_length=50, null=True)
    BP11=models.CharField(max_length=50, null=True)
    RP11=models.CharField(max_length=50, null=True)
    LP11=models.CharField(max_length=50, null=True)
    CP55=models.CharField(max_length=50, null=True)
    TP55=models.CharField(max_length=50, null=True)
    BP55=models.CharField(max_length=50, null=True)
    RP55=models.CharField(max_length=50, null=True)
    LP55=models.CharField(max_length=50, null=True)
    CP54=models.CharField(max_length=50, null=True)
    TP54=models.CharField(max_length=50, null=True)
    BP54=models.CharField(max_length=50, null=True)
    RP54=models.CharField(max_length=50, null=True)
    LP54=models.CharField(max_length=50, null=True)
    CP53=models.CharField(max_length=50, null=True)
    TP53=models.CharField(max_length=50, null=True)
    BP53=models.CharField(max_length=50, null=True)
    RP53=models.CharField(max_length=50, null=True)
    LP53=models.CharField(max_length=50, null=True)
    CP52=models.CharField(max_length=50, null=True)
    TP52=models.CharField(max_length=50, null=True)
    BP52=models.CharField(max_length=50, null=True)
    RP52=models.CharField(max_length=50, null=True)
    LP52=models.CharField(max_length=50, null=True)
    CP51=models.CharField(max_length=50, null=True)
    TP51=models.CharField(max_length=50, null=True)
    BP51=models.CharField(max_length=50, null=True)
    RP51=models.CharField(max_length=50, null=True)
    LP51=models.CharField(max_length=50, null=True)
    CP85=models.CharField(max_length=50, null=True)
    TP85=models.CharField(max_length=50, null=True)
    BP85=models.CharField(max_length=50, null=True)
    RP85=models.CharField(max_length=50, null=True)
    LP85=models.CharField(max_length=50, null=True)
    CP84=models.CharField(max_length=50, null=True)
    TP84=models.CharField(max_length=50, null=True)
    BP84=models.CharField(max_length=50, null=True)
    RP84=models.CharField(max_length=50, null=True)
    LP84=models.CharField(max_length=50, null=True)
    CP83=models.CharField(max_length=50, null=True)
    TP83=models.CharField(max_length=50, null=True)
    BP83=models.CharField(max_length=50, null=True)
    RP83=models.CharField(max_length=50, null=True)
    LP83=models.CharField(max_length=50, null=True)
    CP82=models.CharField(max_length=50, null=True)
    TP82=models.CharField(max_length=50, null=True)
    BP82=models.CharField(max_length=50, null=True)
    RP82=models.CharField(max_length=50, null=True)
    LP82=models.CharField(max_length=50, null=True)
    CP81=models.CharField(max_length=50, null=True)
    TP81=models.CharField(max_length=50, null=True)
    BP81=models.CharField(max_length=50, null=True)
    RP81=models.CharField(max_length=50, null=True)
    LP81=models.CharField(max_length=50, null=True)
    CP48=models.CharField(max_length=50, null=True)
    TP48=models.CharField(max_length=50, null=True)
    BP48=models.CharField(max_length=50, null=True)
    RP48=models.CharField(max_length=50, null=True)
    LP48=models.CharField(max_length=50, null=True)
    CP47=models.CharField(max_length=50, null=True)
    TP47=models.CharField(max_length=50, null=True)
    BP47=models.CharField(max_length=50, null=True)
    RP47=models.CharField(max_length=50, null=True)
    LP47=models.CharField(max_length=50, null=True)
    CP46=models.CharField(max_length=50, null=True)
    TP46=models.CharField(max_length=50, null=True)
    BP46=models.CharField(max_length=50, null=True)
    RP46=models.CharField(max_length=50, null=True)
    LP46=models.CharField(max_length=50, null=True)
    CP45=models.CharField(max_length=50, null=True)
    TP45=models.CharField(max_length=50, null=True)
    BP45=models.CharField(max_length=50, null=True)
    RP45=models.CharField(max_length=50, null=True)
    LP45=models.CharField(max_length=50, null=True)
    CP44=models.CharField(max_length=50, null=True)
    TP44=models.CharField(max_length=50, null=True)
    BP44=models.CharField(max_length=50, null=True)
    RP44=models.CharField(max_length=50, null=True)
    LP44=models.CharField(max_length=50, null=True)
    CP43=models.CharField(max_length=50, null=True)
    TP43=models.CharField(max_length=50, null=True)
    BP43=models.CharField(max_length=50, null=True)
    RP43=models.CharField(max_length=50, null=True)
    LP43=models.CharField(max_length=50, null=True)
    CP42=models.CharField(max_length=50, null=True)
    TP42=models.CharField(max_length=50, null=True)
    BP42=models.CharField(max_length=50, null=True)
    RP42=models.CharField(max_length=50, null=True)
    LP42=models.CharField(max_length=50, null=True)
    CP41=models.CharField(max_length=50, null=True)
    TP41=models.CharField(max_length=50, null=True)
    BP41=models.CharField(max_length=50, null=True)
    RP41=models.CharField(max_length=50, null=True)
    LP41=models.CharField(max_length=50, null=True)
    CP21=models.CharField(max_length=50, null=True)
    TP21=models.CharField(max_length=50, null=True)
    BP21=models.CharField(max_length=50, null=True)
    RP21=models.CharField(max_length=50, null=True)
    LP21=models.CharField(max_length=50, null=True)
    CP22=models.CharField(max_length=50, null=True)
    TP22=models.CharField(max_length=50, null=True)
    BP22=models.CharField(max_length=50, null=True)
    RP22=models.CharField(max_length=50, null=True)
    LP22=models.CharField(max_length=50, null=True)
    CP23=models.CharField(max_length=50, null=True)
    TP23=models.CharField(max_length=50, null=True)
    BP23=models.CharField(max_length=50, null=True)
    RP23=models.CharField(max_length=50, null=True)
    LP23=models.CharField(max_length=50, null=True)
    CP24=models.CharField(max_length=50, null=True)
    TP24=models.CharField(max_length=50, null=True)
    BP24=models.CharField(max_length=50, null=True)
    RP24=models.CharField(max_length=50, null=True)
    LP24=models.CharField(max_length=50, null=True)
    CP25=models.CharField(max_length=50, null=True)
    TP25=models.CharField(max_length=50, null=True)
    BP25=models.CharField(max_length=50, null=True)
    RP25=models.CharField(max_length=50, null=True)
    LP25=models.CharField(max_length=50, null=True)
    CP26=models.CharField(max_length=50, null=True)
    TP26=models.CharField(max_length=50, null=True)
    BP26=models.CharField(max_length=50, null=True)
    RP26=models.CharField(max_length=50, null=True)
    LP26=models.CharField(max_length=50, null=True)
    CP27=models.CharField(max_length=50, null=True)
    TP27=models.CharField(max_length=50, null=True)
    BP27=models.CharField(max_length=50, null=True)
    RP27=models.CharField(max_length=50, null=True)
    LP27=models.CharField(max_length=50, null=True)
    CP28=models.CharField(max_length=50, null=True)
    TP28=models.CharField(max_length=50, null=True)
    BP28=models.CharField(max_length=50, null=True)
    RP28=models.CharField(max_length=50, null=True)
    LP28=models.CharField(max_length=50, null=True)
    CP61=models.CharField(max_length=50, null=True)
    TP61=models.CharField(max_length=50, null=True)
    BP61=models.CharField(max_length=50, null=True)
    RP61=models.CharField(max_length=50, null=True)
    LP61=models.CharField(max_length=50, null=True)
    CP62=models.CharField(max_length=50, null=True)
    TP62=models.CharField(max_length=50, null=True)
    BP62=models.CharField(max_length=50, null=True)
    RP62=models.CharField(max_length=50, null=True)
    LP62=models.CharField(max_length=50, null=True)
    CP63=models.CharField(max_length=50, null=True)
    TP63=models.CharField(max_length=50, null=True)
    BP63=models.CharField(max_length=50, null=True)
    RP63=models.CharField(max_length=50, null=True)
    LP63=models.CharField(max_length=50, null=True)
    CP64=models.CharField(max_length=50, null=True)
    TP64=models.CharField(max_length=50, null=True)
    BP64=models.CharField(max_length=50, null=True)
    RP64=models.CharField(max_length=50, null=True)
    LP64=models.CharField(max_length=50, null=True)
    CP65=models.CharField(max_length=50, null=True)
    TP65=models.CharField(max_length=50, null=True)
    BP65=models.CharField(max_length=50, null=True)
    RP65=models.CharField(max_length=50, null=True)
    LP65=models.CharField(max_length=50, null=True)
    CP71=models.CharField(max_length=50, null=True)
    TP71=models.CharField(max_length=50, null=True)
    BP71=models.CharField(max_length=50, null=True)
    RP71=models.CharField(max_length=50, null=True)
    LP71=models.CharField(max_length=50, null=True)
    CP72=models.CharField(max_length=50, null=True)
    TP72=models.CharField(max_length=50, null=True)
    BP72=models.CharField(max_length=50, null=True)
    RP72=models.CharField(max_length=50, null=True)
    LP72=models.CharField(max_length=50, null=True)
    CP73=models.CharField(max_length=50, null=True)
    TP73=models.CharField(max_length=50, null=True)
    BP73=models.CharField(max_length=50, null=True)
    RP73=models.CharField(max_length=50, null=True)
    LP73=models.CharField(max_length=50, null=True)
    CP74=models.CharField(max_length=50, null=True)
    TP74=models.CharField(max_length=50, null=True)
    BP74=models.CharField(max_length=50, null=True)
    RP74=models.CharField(max_length=50, null=True)
    LP74=models.CharField(max_length=50, null=True)
    CP75=models.CharField(max_length=50, null=True)
    TP75=models.CharField(max_length=50, null=True)
    BP75=models.CharField(max_length=50, null=True)
    RP75=models.CharField(max_length=50, null=True)
    LP75=models.CharField(max_length=50, null=True)
    CP31=models.CharField(max_length=50, null=True)
    TP31=models.CharField(max_length=50, null=True)
    BP31=models.CharField(max_length=50, null=True)
    RP31=models.CharField(max_length=50, null=True)
    LP31=models.CharField(max_length=50, null=True)
    CP32=models.CharField(max_length=50, null=True)
    TP32=models.CharField(max_length=50, null=True)
    BP32=models.CharField(max_length=50, null=True)
    RP32=models.CharField(max_length=50, null=True)
    LP32=models.CharField(max_length=50, null=True)
    CP33=models.CharField(max_length=50, null=True)
    TP33=models.CharField(max_length=50, null=True)
    BP33=models.CharField(max_length=50, null=True)
    RP33=models.CharField(max_length=50, null=True)
    LP33=models.CharField(max_length=50, null=True)
    CP34=models.CharField(max_length=50, null=True)
    TP34=models.CharField(max_length=50, null=True)
    BP34=models.CharField(max_length=50, null=True)
    RP34=models.CharField(max_length=50, null=True)
    LP34=models.CharField(max_length=50, null=True)
    CP35=models.CharField(max_length=50, null=True)
    TP35=models.CharField(max_length=50, null=True)
    BP35=models.CharField(max_length=50, null=True)
    RP35=models.CharField(max_length=50, null=True)
    LP35=models.CharField(max_length=50, null=True)
    CP36=models.CharField(max_length=50, null=True)
    TP36=models.CharField(max_length=50, null=True)
    BP36=models.CharField(max_length=50, null=True)
    RP36=models.CharField(max_length=50, null=True)
    LP36=models.CharField(max_length=50, null=True)
    CP37=models.CharField(max_length=50, null=True)
    TP37=models.CharField(max_length=50, null=True)
    BP37=models.CharField(max_length=50, null=True)
    RP37=models.CharField(max_length=50, null=True)
    LP37=models.CharField(max_length=50, null=True)
    CP38=models.CharField(max_length=50, null=True)
    TP38=models.CharField(max_length=50, null=True)
    BP38=models.CharField(max_length=50, null=True)
    RP38=models.CharField(max_length=50, null=True)
    LP38=models.CharField(max_length=50, null=True)

class Tratamiento(ModeloBase):
    nombre = models.CharField(max_length=100, verbose_name=u'Nombre')
    costo = models.DecimalField(max_digits=30, decimal_places=2, default=0, verbose_name=u'Costo')
    descripcion = models.CharField(max_length=600, verbose_name=u'Nombre')


    class Meta:
        verbose_name = "Tratamiento"
        verbose_name_plural = "Tratamientos"
        ordering = ['id']

    def __str__(self):
        return u'%s - Costo:$%s' % (self.nombre,self.costo)

class Consulta(ModeloBase):
    fecha = models.DateField(verbose_name=u'Fecha' ,auto_now_add=True)
    paciente = models.ForeignKey(Paciente,  on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,  on_delete=models.CASCADE)
    diagnostico_previo = models.TextField(default='', max_length= 600, verbose_name='Diagnostico Previo')
    odontograma = models.ForeignKey(Odontograma,  on_delete=models.CASCADE)
    observacion = models.TextField(default='', max_length=600, verbose_name='Observación')
    tratamientos =  models.ManyToManyField(Tratamiento, verbose_name=u'Tratamientos')
    cancelado = models.BooleanField(default=False)
    def __str__(self):
        return u'Paciente: %s - Fecha: %s ' % (self.paciente, self.fecha)


    def obtener_costo_total(self):
        total_costo = 0
        for costo in self.tratamientos.all():
            total_costo = total_costo + costo.costo
        return  total_costo

    def obtener_iva(self):
        return (float(self.obtener_costo_total()) * 0.12)

    def obtener_subtotal(self):
        return float(self.obtener_costo_total())-float(self.obtener_iva())



    def obtener_total_abonado(self):
        abonos = AbonoPago.objects.filter(consulta=self)
        total_Abonado = abonos.aggregate(Sum('abono'))
        if total_Abonado['abono__sum'] is None:
            total_Abonado = 0
        else:
            total_Abonado = total_Abonado['abono__sum']

        return total_Abonado

    def obtener_saldo_pendiente(self):
        total = self.obtener_costo_total()
        abonado =self.obtener_total_abonado()
        restante = total - abonado
        return restante

    def obtener_ultima_fecha_abonada(self):
        return self.abonopago_set.filter(status=True).last()

class AbonoPago(ModeloBase):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    abono = models.DecimalField(max_digits=30, decimal_places=2, default=0, verbose_name=u'Abono')

    def __str__(self):
        return u'Abonado: %s ' % (self.abono)



class TiempoAntesRecordatorioCorreo(ModeloBase):
    dias_antes = models.CharField(max_length=100, verbose_name=u'Días antes del recordatorio')
    horas_antes = models.CharField(max_length=100, verbose_name=u'Horas antes del recordatorio')
    minutos_antes = models.CharField(max_length=100, verbose_name=u'Minutos antes del recordatorio')

    def __str__(self):
        return u'Días: %s | Horas: %s | Minutos: %s' % (self.dias_antes,self.horas_antes,self.minutos_antes)


