from django import forms


class ModuloForm(forms.Form):
    nombre = forms.CharField(label = 'Nombre', required=True, widget=forms.TextInput(attrs={'formwidth':'50%', 'class':'form-control'}))
    descripcion = forms.CharField(label='Descripción', required=True, widget=forms.TextInput(attrs={'formwidth': '50%','class':' form-control'}))
    ruta = forms.CharField(label='Ruta', required=True, widget=forms.TextInput(attrs={'formwidth': '50%','class':'form-control'}))
    icono = forms.ImageField(label='Icono', widget=forms.ClearableFileInput(attrs={'formwidth': '50%','class':'dropify'}))
    activo = forms.BooleanField(label='Activo', widget=forms.CheckboxInput(attrs={'formwidth': '50%','class':'form-check form-switch ms-2 my-auto is-filled'}))





