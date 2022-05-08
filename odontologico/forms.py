from django import forms


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


class ModuloForm(forms.Form):
    nombre = forms.CharField(label='Nombre', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control uppercase-input', }))
    descripcion = forms.CharField(label='Descripción', required=True,
                                  widget=forms.TextInput(attrs={'class': ' form-control uppercase-input'}))
    ruta = forms.CharField(label='Ruta', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    icono = forms.ImageField(label='Icono', required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'dropify', 'data-allowed-file-extensions': 'PNG png'}))
    activo = forms.BooleanField(label='Activo', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check form-switch ms-2 my-auto is-filled'}))

    def add(self):
        campo_requerido(self, 'icono')

    def editar(self):
        campo_no_requerido(self, 'icono')
