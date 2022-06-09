from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput, ModelChoiceField

from odontologico.models import Genero, Modulo, Paciente, Doctor


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
    nombre1 = forms.CharField(label="1er. Nombre", widget=forms.TextInput(attrs={'class': 'form-control', }))
    nombre2 = forms.CharField(label="2do. Nombre", widget=forms.TextInput(attrs={'class': 'form-control', }))
    apellido1 = forms.CharField(label="Apellido paterno", widget=forms.TextInput(attrs={'class': 'form-control', }))
    apellido2 = forms.CharField(label="Apellido materno", widget=forms.TextInput(attrs={'class': 'form-control', }))
    cedula = forms.CharField(label=u"Cédula", max_length=10, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    genero = forms.ModelChoiceField(label=u"Género", queryset=Genero.objects.filter(status=True),
                                    widget=forms.Select(attrs={'class': 'form-control', }))
    telefono_movil = forms.CharField(label=u"Teléfono móvil", max_length=50,
                                     widget=forms.TextInput(attrs={'class': 'form-control', }))
    telefono_convencional = forms.CharField(label=u"Teléfono Convencional", max_length=50, required=False,
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
            raise ValidationError("La contraseña no coincide.")

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
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    descripcion = forms.CharField(label='Descripción', required=True,
                                  widget=forms.TextInput(attrs={'class': ' form-control '}))
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
    nombre1 = forms.CharField(label='1ª Nombre', required=True,
                             widget=forms.TextInput(attrs={'class': ' form-control', }))
    nombre2 = forms.CharField(label='2ª Nombre', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    apellido1 = forms.CharField(label='1ª Apellido', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    apellido2 = forms.CharField(label='2º Apellido', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', }))
    email = forms.CharField(label=u"Correo electrónico", max_length=200, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control',}))
    cedula = forms.CharField(label=u"Cédula", max_length=10, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',}))
    genero = forms.ModelChoiceField(label=u"Gènero",required=True, queryset=Genero.objects.filter(status=True),
                                  widget=forms.Select(attrs={'class': 'form-control',}))

    telefono_movil = forms.CharField(label=u"Teléfono móvil", max_length=50, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'(99 123 1234)'}))
    telefono_convencional = forms.CharField(label=u"Teléfono fijo", max_length=50, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control ',}))


    def editar(self):
        campo_solo_lectura(self, 'cedula')
        campo_solo_lectura(self, 'genero')

class AccesoModuloForm(forms.Form):
    grupo = forms.ModelChoiceField(label=u"Grupo", queryset=Group.objects.all(), widget=forms.Select(attrs={'class': 'form-control', }))
    modulo = forms.ModelChoiceField(label=u"Módulo", queryset=Modulo.objects.filter(status=True, activo = True), widget=forms.Select(attrs={'class': 'form-control', }))
    activo = forms.BooleanField(label='Activo', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check form-switch ms-2 my-auto is-filled','checked':'checked'}))


class AgendarCitaForm(forms.Form):
    paciente = ModelChoiceField(label=u'Paciente', queryset=Paciente.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control', }))
    doctor = ModelChoiceField(label=u'Especialista', queryset=Doctor.objects.filter(status=True),  widget=forms.Select(attrs={'class': 'form-control', }))
    fecha_cita = forms.DateField(label=u"Fecha de la cita", input_formats=['%d-%m-%Y'], widget=DateTimeInput(format='%d-%m-%Y', attrs={'class': 'form-control'}), )
    hora_cita = forms.TimeField(label=u"Hora de la cita", input_formats=['%H:%M'], widget=DateTimeInput(format='%H:%M', attrs={'class': 'form-control'}))
