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
        # ✅ Agregamos trimestre
        fields = ['articuloDe', 'carpeta', 'trimestre', 'titulo_archivo', 'ano', 'liga', 'archivo']
        widgets = {
            'articuloDe': forms.Select(attrs={'class': 'form-control'}),
            'trimestre': forms.Select(attrs={'class': 'form-control'}),  # ✅ nuevo
            'titulo_archivo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del archivo (opcional)'
            }),
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
            self.fields['articuloDe'].disabled = True

        # 2) Año obligatorio
        self.fields['ano'].required = True

        # ✅ 2.1) Trimestre: (decide si lo quieres obligatorio siempre o solo con archivo)
        # Opción A (recomendada): obligatorio solo si se sube archivo (validamos en clean)
        self.fields['trimestre'].required = False

        # 3) Cargar carpetas y mostrarlas con indentación (principal/sub/subsub)
        qs = CarpetaTransparencia.objects.select_related('padre').order_by('orden', 'nombre')
        self.fields['carpeta'].queryset = qs
        self.fields['carpeta'].label_from_instance = self._label_carpeta

    def _label_carpeta(self, carpeta):
        depth = 0
        p = carpeta.padre
        while p:
            depth += 1
            p = p.padre
        prefix = "— " * depth
        return f"{prefix}{carpeta.nombre}"

    def clean(self):
        cleaned_data = super().clean()
        liga = cleaned_data.get('liga')
        archivo = cleaned_data.get('archivo')
        ano = cleaned_data.get('ano')
        trimestre = cleaned_data.get('trimestre')

        # 1) Debe existir al menos liga o archivo
        if not liga and not archivo:
            raise forms.ValidationError("Debe ingresar al menos un enlace o un archivo.")

        # 2) Año obligatorio
        if not ano:
            self.add_error('ano', "El año fiscal es obligatorio.")

        # ✅ 3) Trimestre: valida 1-4 y/o obligatorio si hay archivo
        # Recomendación: si hay archivo, exige trimestre (para carpeta física)
        if archivo:
            if not trimestre:
                self.add_error('trimestre', "El trimestre es obligatorio cuando subes un archivo.")
            else:
                try:
                    t = int(trimestre)
                except (TypeError, ValueError):
                    self.add_error('trimestre', "Trimestre inválido.")
                else:
                    if t not in (1, 2, 3, 4):
                        self.add_error('trimestre', "El trimestre debe ser 1, 2, 3 o 4.")

        # Si quieres exigir trimestre también para ligas, cambia a:
        # if not trimestre: self.add_error('trimestre', "...")

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