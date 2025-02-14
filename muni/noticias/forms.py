from django import forms
from .models import Noticia
from django_ckeditor_5.widgets import CKEditor5Widget

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
            'imagenes_galeria': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        contenido = CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              )
        