from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput, ModelChoiceField

from odontologico.models import Genero, Modulo, Paciente, Doctor, Horario_hora, Tratamiento


def deshabilitar_campo(form, campo):
    form.fields[campo].widget.attrs['readonly'] = True
    form.fields[campo].widget.attrs['disabled'] = True


def campo_requerido(form, campo):
    form.fields[campo].widget.attrs['required'] = True


def campo_no_requerido(form, campo):
    form.fields[campo].widget.attrs['required'] = False


def habilitar_campo(form, campo):
    form.fields[campo].widget.attrs['readonly'] = False
    form.fields[campo].widget.attrs['disabled'] = False


def campo_solo_lectura(form, campo):
    form.fields[campo].widget.attrs['readonly'] = True


class RegistroUsuarioForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            self.fields['password1'].widget.attrs['class'] = "form-control"
            self.fields['password2'].widget.attrs['class'] = "form-control"

    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', }))
    nombre1 = forms.CharField(label="1er. Nombre", widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_letras(event)', }))
    nombre2 = forms.CharField(label="2do. Nombre", widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_letras(event)', }))
    apellido1 = forms.CharField(label="Apellido paterno", widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_letras(event)', }))
    apellido2 = forms.CharField(label="Apellido materno", widget=forms.TextInput(attrs={'class': 'form-control', 'onKeyPress' : 'return solo_letras(event)',}))
    cedula = forms.CharField(label=u"C??dula", max_length=10, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_numeros(event)',}))
    genero = forms.ModelChoiceField(label=u"G??nero", queryset=Genero.objects.filter(status=True),
                                    widget=forms.Select(attrs={'class': 'form-control', }))
    telefono_movil = forms.CharField(label=u"Tel??fono m??vil", max_length=50,
                                     widget=forms.TextInput(attrs={'class': 'form-control', }))
    telefono_convencional = forms.CharField(label=u"Tel??fono Convencional", max_length=50, required=False,
                                            widget=forms.TextInput(attrs={'class': 'form-control', }))


    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Nombre de usuario ya existe.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email ya existe")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("La contrase??a no coincide.")

        return password2

    class Meta:
        model = User
        fields = ("username", "email",)

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',

                }
            ),
        }

class ModuloForm(forms.Form):
    nombre = forms.CharField(label='Nombre', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_letras(event)', }))
    descripcion = forms.CharField(label='Descripci??n', required=True,
                                  widget=forms.TextInput(attrs={'class': ' form-control ','onKeyPress' : 'return solo_letras(event)', }))
    ruta = forms.CharField(label='Ruta', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    icono = forms.ImageField(label='Icono', required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'dropify', 'data-allowed-file-extensions': 'PNG png'}))
    activo = forms.BooleanField(label='Activo', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check form-switch ms-2 my-auto is-filled'}))

    def add(self):
        campo_requerido(self, 'icono')

    def editar(self):
        campo_no_requerido(self, 'icono')


class PersonaForm(forms.Form):
    nombre1 = forms.CharField(label='1?? Nombre', required=True,
                             widget=forms.TextInput(attrs={'class': ' form-control','onKeyPress' : 'return solo_letras(event)',  }))
    nombre2 = forms.CharField(label='2?? Nombre', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_letras(event)',  }))
    apellido1 = forms.CharField(label='1?? Apellido', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_letras(event)', }))
    apellido2 = forms.CharField(label='2?? Apellido', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_letras(event)',  }))
    email = forms.CharField(label="Correo electr??nico", max_length=200, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control',}))
    cedula = forms.CharField(label="C??dula", max_length=10, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_numeros(event)',}))
    genero = forms.ModelChoiceField(label="G??nero",required=True, queryset=Genero.objects.filter(status=True),
                                  widget=forms.Select(attrs={'class': 'form-control',}))

    telefono_movil = forms.CharField(label="Tel??fono m??vil", max_length=50, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'(99 123 1234)'}))
    telefono_convencional = forms.CharField(label=u"Tel??fono fijo", max_length=50, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control ',}))


    def editar(self):
        campo_solo_lectura(self, 'cedula')
        campo_solo_lectura(self, 'genero')

class AccesoModuloForm(forms.Form):
    grupo = forms.ModelChoiceField(label="Grupo", queryset=Group.objects.all(), widget=forms.Select(attrs={'class': 'form-control', }))
    modulo = forms.ModelChoiceField(label="M??dulo", queryset=Modulo.objects.filter(status=True, activo = True), widget=forms.Select(attrs={'class': 'form-control', }))
    activo = forms.BooleanField(label='Activo', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check form-switch ms-2 my-auto is-filled','checked':'checked'}))


class AgendarCitaForm(forms.Form):
    paciente = ModelChoiceField(label='Paciente', queryset=Paciente.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control', }))
    doctor = ModelChoiceField(label='Especialista', queryset=Doctor.objects.filter(status=True),  widget=forms.Select(attrs={'class': 'form-control', }))
    fecha_cita = forms.DateField(label="Fecha de la cita",initial=datetime.now().date(), input_formats=['%d-%m-%Y'], widget=DateTimeInput(format='%d-%m-%Y', attrs={'class': 'form-control'}) )
    hora_cita = forms.ModelChoiceField(label="Hora de la cita", queryset=Horario_hora.objects.filter(status=True, activo=True), widget=forms.Select(attrs={'class': 'form-control', }) )

    def editar(self):
        campo_solo_lectura(self, 'paciente')
        campo_solo_lectura(self, 'doctor')


class ConsultaForm(forms.Form):
    diagnostico_previo =  forms.CharField(label='Diagnostio Previo', required=False,
                             widget=forms.Textarea(attrs={'class': 'form-control', }))
    tratamientos = forms.ModelMultipleChoiceField(Tratamiento.objects.filter(status=True), label=u'Tratamientos', required=False,  widget=forms.SelectMultiple(attrs={'class': 'duallistbox form-control'}))
    observacion =  forms.CharField(label='Observacion', required=False, widget=forms.Textarea(attrs={'class': 'form-control', }))


class AgendarCitaOnlineForm(forms.Form):
    doctor = ModelChoiceField(label='Especialista', queryset=Doctor.objects.filter(status=True),  widget=forms.Select(attrs={'class': 'form-control', }))
    fecha_cita = forms.DateField(label="Fecha de la cita",initial=datetime.now().date(), input_formats=['%d-%m-%Y'], widget=DateTimeInput(format='%d-%m-%Y', attrs={'class': 'form-control'}) )
    hora_cita = forms.ModelChoiceField(label="Hora de la cita", queryset=Horario_hora.objects.filter(status=True, activo=True), widget=forms.Select(attrs={'class': 'form-control', }) )


class TratamientoForm(forms.Form):
    nombre =  forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_letras(event)', }))

    costo = forms.DecimalField(initial='0.00', label='Costo',required=True, widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_digitos(event)',}))

    descripcion =  forms.CharField(label='Descripci??n', required=False,widget=forms.Textarea(attrs={'class': 'form-control', }))



class AbonarCuotaForm(forms.Form):

    abono = forms.DecimalField(initial='0.00', label='Abono',required=True, widget=forms.TextInput(attrs={'class': 'form-control','onKeyPress' : 'return solo_digitos(event)',}))



class HorarioHoraForm(forms.Form):
    hora_inicio = forms.TimeField(label="Hora Inicio", input_formats=['%H:%M'],
                                  widget=DateTimeInput(format='%H:%M',
                                                       attrs={'class': 'form-control'}))
    hora_fin = forms.TimeField(label="Hora Fin", input_formats=['%H:%M'],
                               widget=DateTimeInput(format='%H:%M',
                                                    attrs={'class': 'form-control'}))

    activo = forms.BooleanField(label='Activo', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check form-switch ms-2 my-auto is-filled', 'checked': 'checked'}))

