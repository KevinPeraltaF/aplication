from django import forms


class ModuloForm(forms.Form):
    nombre = forms.CharField(label = 'Nombre', required=True, widget=forms.TextInput(attrs={'class':'form-control',}))
    descripcion = forms.CharField(label='Descripción', required=True, widget=forms.TextInput(attrs={'class':' form-control'}))
    ruta = forms.CharField(label='Ruta', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    icono = forms.ImageField(label='Icono', widget=forms.ClearableFileInput(attrs={'class':'dropify'}))
    activo = forms.BooleanField(label='Activo', widget=forms.CheckboxInput(attrs={'class':'form-check form-switch ms-2 my-auto is-filled'}))





