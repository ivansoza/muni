from django import forms
from .models import Noticia, ImagenGaleria
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import modelformset_factory

class NoticiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["contenido"].required = False
    
    class Meta:
        model = Noticia
        fields = ['titulo', 'contenido', 'autor', 'categoria', 'imagen', 'imagenes_galeria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la noticia'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        contenido = CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5", "id": "id_contenido"}, config_name="extends"
              )
        
class ImagenGaleriaForm(forms.ModelForm):
    class Meta:
        model = ImagenGaleria
        fields = ['imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

# FormSet para múltiples imágenes
ImagenGaleriaFormSet = modelformset_factory(ImagenGaleria, form=ImagenGaleriaForm, extra=4)  # Permite subir hasta 4 imágenes