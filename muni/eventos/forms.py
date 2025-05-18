from django import forms
from .models import Articulo, Categoria, Autor
from django_ckeditor_5.widgets import CKEditor5Widget

class ArticuloForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contenido"].required = False

    class Meta:
        model = Articulo
        fields = ['titulo', 'abstract', 'contenido', 'imagen', 'categoria', 'etiquetas', 'autor', 'destacado', 'tiempo_lectura', 'video_url']

        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Introduce el título del artículo',
                'class': 'form-control'
            }),
            'abstract': forms.Textarea(attrs={
                'placeholder': 'Escribe un resumen del artículo',
                'class': 'form-control',
                'rows': 4
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            # Usamos CheckboxSelectMultiple para las categorías
           'categoria': forms.Select(attrs={
                'class': 'form-control', 'id':'id_categoria'
            }),  
            'etiquetas': forms.TextInput(attrs={
                'placeholder': 'Escribe etiquetas separadas por comas',
                'class': 'form-control'
            }),
            'autor': forms.Select(attrs={
                'class': 'form-control', 'id':'id_autor'
            }),
            'destacado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tiempo_lectura': forms.NumberInput(attrs={
                'placeholder': 'Tiempo estimado de lectura en minutos',
                'class': 'form-control',
                'min': 1
            }),
            'video_url': forms.TextInput(attrs={
                'placeholder': 'Pega la url del video',
                'class': 'form-control'
            }),
        }
        contenido = CKEditor5Widget(
            attrs={"class": "django_ckeditor_5", "id": "id_contenido"}, config_name="extends"
        )

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if not titulo:
            raise forms.ValidationError('El título es obligatorio.')
        return titulo

    def clean_etiquetas(self):
        etiquetas = self.cleaned_data.get('etiquetas')
        if etiquetas:
            etiquetas_lista = [etiqueta.strip() for etiqueta in etiquetas.split(',')]
            return ', '.join(etiquetas_lista)
        return etiquetas

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre_completo', 'perfil', 'trayectoria', 'fotografia']

        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'placeholder': 'Introduce el nombre completo del autor',
                'class': 'form-control'
            }),
            'perfil': forms.TextInput(attrs={
                'placeholder': 'Introduce el perfil del autor',
                'class': 'form-control'
            }),
            'trayectoria': forms.Textarea(attrs={
                'placeholder': 'Introduce la trayectoria del autor',
                'class': 'form-control',
                'rows': 4
            }),
            'fotografia': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }