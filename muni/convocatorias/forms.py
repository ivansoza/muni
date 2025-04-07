from django import forms
from .models import Convocatoria, ArchivoConvocatoria
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import modelformset_factory

class ConvocatoriaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["contenido"].required = False
    class Meta:
        model = Convocatoria
        fields = [
            'titulo', 'categoria', 'estado', 'imagen',
            'fecha_apertura', 'fecha_cierre',
            'descripcion', 'contenido',
            'departamento', 'email', 'telefono', 'horarios_atencion'
        ]
        widgets = {
            'fecha_apertura': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cierre': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
        contenido = CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5", "id": "id_contenido"}, config_name="extends"
              )

class ArchivoConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = ArchivoConvocatoria
        fields = ['archivo', 'nombre']
        widgets = {
            'archivo': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',  # tipos permitidos
                'class': 'file-input'
            }),
        }

ArchivoConvocatoriaFormSet = modelformset_factory(
    ArchivoConvocatoria,
    form=ArchivoConvocatoriaForm,
    extra=1,  # Puedes cambiar esto para permitir más archivos
    can_delete=True
)
