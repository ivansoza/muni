from django import forms
from .models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia, ListaObligaciones, ArticuloLiga, LigaArchivo

class SeccionTransparenciaForm(forms.ModelForm):
    class Meta:
        model = SeccionTransparencia
        fields = ['nombre', 'descripcion','imagen', 'usa_ejercicios', 'usa_meses']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la sección'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción'}),
            'usa_ejercicios': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'usa_meses': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'usa_ejercicios': 'Marca esta casilla si esta sección debe manejar ejercicios fiscales.',
            'usa_meses': 'Marca esta casilla si esta sección requiere dividir los registros por meses.',
        }
        # Personaliza los textos de ayuda para incluir clases adicionales
        error_messages = {
            'usa_ejercicios': {'help_text': 'help-text-custom'},
            'usa_meses': {'help_text': 'help-text-custom'}
        }

class EjercicioFiscalForm(forms.ModelForm):
    class Meta:
        model = EjercicioFiscal
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción del ejercicio fiscal'}),
        }

class DocumentoTransparenciaForm(forms.ModelForm):
    """Formulario para registrar un nuevo documento de transparencia"""

    class Meta:
        model = DocumentoTransparencia
        fields = ['titulo', 'descripcion', 'archivo', 'año', 'mes']
        widgets = {
            'mes': forms.Select(attrs={'class': 'form-control'}),  # Agregamos estilo a mes
            'año': forms.NumberInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.seccion = kwargs.pop('seccion', None)  # Extraemos la sección
        self.ejercicio_fiscal = kwargs.pop('ejercicio_fiscal', None)  # Extraemos el ejercicio fiscal
        super().__init__(*args, **kwargs)
         # Si la sección no usa ejercicios, ocultamos el campo de año
        if self.seccion and not self.seccion.usa_ejercicios:
            self.fields.pop('año')

        # Si la sección no usa meses, ocultamos el campo de mes
        if self.seccion and not self.seccion.usa_meses:
            self.fields.pop('mes')
    
class ListaObligacionesForm(forms.ModelForm):
    class Meta:
        model = ListaObligaciones
        fields = ['titulo', 'articulo']
        labels = {
            'titulo': 'Título de la lista',
            'articulo': 'Título de artículo',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Obligaciones de transparencia'
            }),
            'articulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Artículo 70 de la Ley General'
            }),
        }


class ArticuloLigaForm(forms.ModelForm):
    class Meta:
        model = ArticuloLiga
        fields = ['lista_obligaciones', 'articulo_fraccion']
        widgets = {
            'lista_obligaciones': forms.Select(attrs={'class': 'form-control'}),
            'articulo_fraccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        lista_obligacion_id = kwargs.pop('lista_obligacion_id', None)
        super().__init__(*args, **kwargs)
        
        if lista_obligacion_id:
            self.fields['lista_obligaciones'].queryset = ListaObligaciones.objects.filter(id=lista_obligacion_id)
            self.fields['lista_obligaciones'].initial = lista_obligacion_id

class ArticuloLigaArchivoForm(forms.ModelForm):
    class Meta:
        model = LigaArchivo
        fields = ['articuloDe', 'ano', 'liga', 'archivo']
        widgets = {
            'articuloDe': forms.Select(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Año fiscal', 'min': 1900, 'max': 2100}),
            'liga': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el enlace completo del artículo'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'custom-file-input', 'id': 'customFile'}),
        }
    
    def __init__(self, *args, **kwargs):
        articulo_id = kwargs.pop('articuloDe_id', None)  # Asegúrate de que esto coincida con la clave pasada en kwargs
        super().__init__(*args, **kwargs)
        
        if articulo_id:
            self.fields['articuloDe'].queryset = ArticuloLiga.objects.filter(id=articulo_id)
            self.fields['articuloDe'].initial = articulo_id
