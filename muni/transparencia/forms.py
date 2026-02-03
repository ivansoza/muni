from django import forms

from reportes.models import ReporteAlcantarillado, ReporteAlumbradoPublico, ReporteBache, ReporteServicioAgua
from .models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia, ListaObligaciones, ArticuloLiga, LigaArchivo, CarpetaTransparencia

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
        fields = ['titulo']
        labels = {
            'titulo': 'Título de la carpeta',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Obligaciones de transparencia'
            }),
        }


class ArticuloLigaForm(forms.ModelForm):
    class Meta:
        model = ArticuloLiga
        fields = ['lista_obligaciones', 'articulo_fraccion']
        widgets = {
            'lista_obligaciones': forms.Select(attrs={
                'class': 'form-control',
            }),
            'articulo_fraccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Artículo 70 Fracción I'
            }),
        }

    def __init__(self, *args, **kwargs):
        lista_obligacion_id = kwargs.pop('lista_obligacion_id', None)
        super().__init__(*args, **kwargs)

        if lista_obligacion_id:
            self.fields['lista_obligaciones'].queryset = ListaObligaciones.objects.filter(id=lista_obligacion_id)
            self.fields['lista_obligaciones'].initial = lista_obligacion_id

class ArticuloLigaArchivoForm(forms.ModelForm):
    carpeta = forms.ModelChoiceField(
        queryset=CarpetaTransparencia.objects.none(),
        required=False,
        label="Carpeta (opcional)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = LigaArchivo
        fields = ['articuloDe', 'carpeta', 'titulo_archivo', 'ano', 'liga', 'archivo']
        widgets = {
            'articuloDe': forms.Select(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Año fiscal',
                'min': 1900,
                'max': 2100
            }),
            'liga': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el enlace completo del artículo'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input',
                'id': 'customFile'
            }),
        }

    def __init__(self, *args, **kwargs):
        articulo_id = kwargs.pop('articuloDe_id', None)
        super().__init__(*args, **kwargs)

        # 1) Si viene articulo_id, encierra articuloDe al artículo fijo
        if articulo_id:
            self.fields['articuloDe'].queryset = ArticuloLiga.objects.filter(id=articulo_id)
            self.fields['articuloDe'].initial = articulo_id
            self.fields['articuloDe'].disabled = True  # evita que lo cambien en UI

        # 2) Año obligatorio
        self.fields['ano'].required = True

        # 3) Cargar carpetas y mostrarlas con indentación (principal/sub/subsub)
        qs = CarpetaTransparencia.objects.select_related('padre').order_by('orden', 'nombre')
        self.fields['carpeta'].queryset = qs
        self.fields['carpeta'].label_from_instance = self._label_carpeta

    def _label_carpeta(self, carpeta):
        # Indentación por profundidad + ruta completa (muy claro para admin)
        depth = 0
        p = carpeta.padre
        while p:
            depth += 1
            p = p.padre
        prefix = "— " * depth
        # Si quieres ruta completa: carpeta.ruta_legible()
        return f"{prefix}{carpeta.nombre}"

    def clean(self):
        cleaned_data = super().clean()
        liga = cleaned_data.get('liga')
        archivo = cleaned_data.get('archivo')
        ano = cleaned_data.get('ano')

        # 1) Debe existir al menos liga o archivo (pero no es obligatorio que sean ambos)
        if not liga and not archivo:
            raise forms.ValidationError("Debe ingresar al menos un enlace o un archivo.")

        # 2) Año obligatorio (ya es required, pero lo reforzamos)
        if not ano:
            self.add_error('ano', "El año fiscal es obligatorio.")

        # 3) (Opcional) Si el usuario puso liga y archivo, lo permitimos.
        # Si quisieras forzar solo uno, aquí lo validarías.

        return cleaned_data




class _ReporteBaseForm(forms.ModelForm):
    """Config común: mismos campos + widgets ocultos"""
    class Meta:
        fields = (
            "nombre_solicitante",
            "descripcion",
            "foto",
            "ubicacion",
            "latitud",
            "longitud",
            "place_id",
        )
        widgets = {
            "latitud":  forms.HiddenInput(),
            "longitud": forms.HiddenInput(),
            "place_id": forms.HiddenInput(),
        }

# ───────────────────  Formularios concretos ────────────────────
class ReporteServicioAguaForm(_ReporteBaseForm):
    class Meta(_ReporteBaseForm.Meta):
        model = ReporteServicioAgua


class ReporteBacheForm(_ReporteBaseForm):
    class Meta(_ReporteBaseForm.Meta):
        model = ReporteBache


class ReporteAlcantarilladoForm(_ReporteBaseForm):
    class Meta(_ReporteBaseForm.Meta):
        model = ReporteAlcantarillado


class ReporteAlumbradoPublicoForm(_ReporteBaseForm):
    class Meta(_ReporteBaseForm.Meta):
        model = ReporteAlumbradoPublico