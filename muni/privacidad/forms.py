from django import forms
from django.forms import inlineformset_factory
from .models import AvisoDePrivacidad, ArchivoRelacionado

class AvisoDePrivacidadForm(forms.ModelForm):
    class Meta:
        model  = AvisoDePrivacidad
        fields = ['area', 'descripcion']
        widgets = {
            'area'       : forms.TextInput(attrs={
                'placeholder': 'Área responsable (ej. Dirección de Transparencia)'}),
            'descripcion': forms.TextInput(attrs={
                'placeholder': 'Descripción breve del aviso'}),
        }

class ArchivoRelacionadoForm(forms.ModelForm):
    class Meta:
        model  = ArchivoRelacionado
        fields = ['archivo', 'descripcion']
        widgets = {
            # el placeholder para un FileInput no se muestra en todos los navegadores,
            # pero lo incluimos por consistencia
            'archivo'    : forms.ClearableFileInput(attrs={
                'placeholder': 'Selecciona un archivo PDF, DOCX, etc.'}),
            'descripcion': forms.TextInput(attrs={
                'placeholder': 'Descripción del archivo (opcional)'}),
        }

ArchivoRelacionadoFormSet = inlineformset_factory(
    AvisoDePrivacidad,
    ArchivoRelacionado,
    form=ArchivoRelacionadoForm,
    extra=1,
    can_delete=False   # seguimos sin DELETE en BD, solo quitamos en el DOM
)