from django import forms
from .models import MiembroGabinete, MiembroGabineteCoordinadoresDif, MiembroGabineteDirectores, MiembroGabinetePresidentesComu, MiembroGabineteRegidores
from django.utils.translation import gettext_lazy as _

class MiembroGabineteForm(forms.ModelForm):
    class Meta:
        model = MiembroGabinete
        fields = [
            'municipio',
            'dependencia',
            'nombre',
            'cargo',
            'status',
            'orden',
            'numero_contacto',
            'correo_electronico',
            'pagina_web',
            'telefono',
            'horario',
            'semblanza',
            'formacion_academica',
            'experiencia',
            'area',
            'descripcion_area',
            'imagen',
        ]
        
        labels = {
            'municipio': _('Municipio'),
            'dependencia': _('Dependencia'),
            'nombre': _('Nombre Completo'),
            'cargo': _('Cargo Oficial'),
            'status': _('Estado Actual'),
            'orden': _('Orden de Visualización'),
            'numero_contacto': _('Número de Contacto Directo'),
            'correo_electronico': _('Correo Electrónico Institucional'),
            'pagina_web': _('Sitio Web'),
            'telefono': _('Teléfono Oficina'),
            'horario': _('Horario de Atención'),
            'semblanza': _('Descripción Profesional'),
            'formacion_academica': _('Formación Académica'),
            'experiencia': _('Experiencia Profesional'),
            'area': _('Área de Responsabilidad'),
            'descripcion_area': _('Descripción del Área'),
            'imagen': _('Fotografía Oficial'),
        }
        
        help_texts = {
            'orden': _('Número que determina la posición en el listado (menor número = mayor prioridad)'),
            'numero_contacto': _('Formato recomendado: +52 (123) 456-7890'),
            'correo_electronico': _('Dirección de correo oficial para contacto público'),
            'imagen': _('Imagen profesional con fondo claro (tamaño recomendado: 400x600px)'),
            'semblanza': _('Descripción breve de la trayectoria profesional'),
        }
        
        widgets = {
            'municipio': forms.Select(attrs={
                'class': 'form-select shadow-sm',
                'data-bs-toggle': 'tooltip',
                'title': 'Seleccione el municipio correspondiente'
            }),
            'dependencia': forms.Select(attrs={
                'class': 'form-select shadow-sm',
                'data-bs-toggle': 'tooltip', 
                'title': 'Seleccione la dependencia a la que pertenece'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Lic. Juan Pérez González',
                'autocomplete': 'name'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Director de Desarrollo Social'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select shadow-sm'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm',
                'min': 1,
                'placeholder': 'Ej. 1, 2, 3...'
            }),
            'numero_contacto': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. +52 (123) 456-7890',
                'pattern': r'[\d\s\+\(\)\-\.]+',
                'autocomplete': 'tel'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'ejemplo@gobierno.gob.mx',
                'autocomplete': 'email'
            }),
            'pagina_web': forms.URLInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'https://www.ejemplo.gob.mx',
                'autocomplete': 'url'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. (123) 456-7890',
                'pattern': r'[\d\s\+\(\)\-\.]+',
            }),
            'horario': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Lunes a Viernes 9:00 - 17:00'
            }),
            'semblanza': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 5,
                'placeholder': 'Breve descripción de la trayectoria profesional del funcionario...'
            }),
            'formacion_academica': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Detalle los estudios y certificaciones obtenidas...'
            }),
            'experiencia': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Detalle la experiencia laboral relevante...'
            }),
            'area': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Desarrollo Económico'
            }),
            'descripcion_area': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Descripción de las funciones y responsabilidades del área...'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control shadow-sm',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar campos obligatorios
        required_fields = ['municipio', 'dependencia', 'nombre', 'cargo', 'status']
        for field_name in required_fields:
            self.fields[field_name].required = True
            if field_name in self.fields and 'class' in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['class'] += ' border-primary'
        
        # Campos opcionales pueden tener un estilo diferente
        for field_name, field in self.fields.items():
            if not field.required:
                field.label = f"{field.label} (Opcional)"


class MiembroGabineteRegidorForm(forms.ModelForm):
    class Meta:
        model = MiembroGabineteRegidores
        fields = [
            'municipio',
            'dependencia',
            'nombre',
            'cargo',
            'status',
            'orden',
            'numero_contacto',
            'correo_electronico',
            'pagina_web',
            'telefono',
            'horario',
            'semblanza',
            'formacion_academica',
            'experiencia',
            'area',
            'descripcion_area',
            'imagen',
        ]
        
        labels = {
            'municipio': _('Municipio'),
            'dependencia': _('Dependencia'),
            'nombre': _('Nombre Completo'),
            'cargo': _('Cargo Oficial'),
            'status': _('Estado Actual'),
            'orden': _('Orden de Visualización'),
            'numero_contacto': _('Número de Contacto Directo'),
            'correo_electronico': _('Correo Electrónico Institucional'),
            'pagina_web': _('Sitio Web'),
            'telefono': _('Teléfono Oficina'),
            'horario': _('Horario de Atención'),
            'semblanza': _('Descripción Profesional'),
            'formacion_academica': _('Formación Académica'),
            'experiencia': _('Experiencia Profesional'),
            'area': _('Área de Responsabilidad'),
            'descripcion_area': _('Descripción del Área'),
            'imagen': _('Fotografía Oficial'),
        }
        
        help_texts = {
            'orden': _('Número que determina la posición en el listado (menor número = mayor prioridad)'),
            'numero_contacto': _('Formato recomendado: +52 (123) 456-7890'),
            'correo_electronico': _('Dirección de correo oficial para contacto público'),
            'imagen': _('Imagen profesional con fondo claro (tamaño recomendado: 400x600px)'),
            'semblanza': _('Descripción breve de la trayectoria profesional'),
        }
        
        widgets = {
            'municipio': forms.Select(attrs={
                'class': 'form-select shadow-sm',
                'data-bs-toggle': 'tooltip',
                'title': 'Seleccione el municipio correspondiente'
            }),
            'dependencia': forms.Select(attrs={
                'class': 'form-select shadow-sm',
                'data-bs-toggle': 'tooltip', 
                'title': 'Seleccione la dependencia a la que pertenece'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Lic. Juan Pérez González',
                'autocomplete': 'name'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Director de Desarrollo Social'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select shadow-sm'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm',
                'min': 1,
                'placeholder': 'Ej. 1, 2, 3...'
            }),
            'numero_contacto': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. +52 (123) 456-7890',
                'pattern': r'[\d\s\+\(\)\-\.]+',
                'autocomplete': 'tel'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'ejemplo@gobierno.gob.mx',
                'autocomplete': 'email'
            }),
            'pagina_web': forms.URLInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'https://www.ejemplo.gob.mx',
                'autocomplete': 'url'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. (123) 456-7890',
                'pattern': r'[\d\s\+\(\)\-\.]+',
            }),
            'horario': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Lunes a Viernes 9:00 - 17:00'
            }),
            'semblanza': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 5,
                'placeholder': 'Breve descripción de la trayectoria profesional del funcionario...'
            }),
            'formacion_academica': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Detalle los estudios y certificaciones obtenidas...'
            }),
            'experiencia': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Detalle la experiencia laboral relevante...'
            }),
            'area': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Desarrollo Económico'
            }),
            'descripcion_area': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Descripción de las funciones y responsabilidades del área...'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control shadow-sm',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar campos obligatorios
        required_fields = ['municipio', 'dependencia', 'nombre', 'cargo', 'status']
        for field_name in required_fields:
            self.fields[field_name].required = True
            if field_name in self.fields and 'class' in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['class'] += ' border-primary'
        
        # Campos opcionales pueden tener un estilo diferente
        for field_name, field in self.fields.items():
            if not field.required:
                field.label = f"{field.label} (Opcional)"



class MiembroGabineteDirectorForm(forms.ModelForm):
    class Meta:
        model = MiembroGabineteDirectores
        fields = [
            'municipio',
            'dependencia',
            'nombre',
            'cargo',
            'status',
            'orden',
            'numero_contacto',
            'correo_electronico',
            'pagina_web',
            'telefono',
            'horario',
            'semblanza',
            'formacion_academica',
            'experiencia',
            'area',
            'descripcion_area',
            'imagen',
        ]
        
        labels = {
            'municipio': _('Municipio'),
            'dependencia': _('Dependencia'),
            'nombre': _('Nombre Completo'),
            'cargo': _('Cargo Oficial'),
            'status': _('Estado Actual'),
            'orden': _('Orden de Visualización'),
            'numero_contacto': _('Número de Contacto Directo'),
            'correo_electronico': _('Correo Electrónico Institucional'),
            'pagina_web': _('Sitio Web'),
            'telefono': _('Teléfono Oficina'),
            'horario': _('Horario de Atención'),
            'semblanza': _('Descripción Profesional'),
            'formacion_academica': _('Formación Académica'),
            'experiencia': _('Experiencia Profesional'),
            'area': _('Área de Responsabilidad'),
            'descripcion_area': _('Descripción del Área'),
            'imagen': _('Fotografía Oficial'),
        }
        
        help_texts = {
            'orden': _('Número que determina la posición en el listado (menor número = mayor prioridad)'),
            'numero_contacto': _('Formato recomendado: +52 (123) 456-7890'),
            'correo_electronico': _('Dirección de correo oficial para contacto público'),
            'imagen': _('Imagen profesional con fondo claro (tamaño recomendado: 400x600px)'),
            'semblanza': _('Descripción breve de la trayectoria profesional'),
        }
        
        widgets = {
            'municipio': forms.Select(attrs={
                'class': 'form-select shadow-sm',
                'data-bs-toggle': 'tooltip',
                'title': 'Seleccione el municipio correspondiente'
            }),
            'dependencia': forms.Select(attrs={
                'class': 'form-select shadow-sm',
                'data-bs-toggle': 'tooltip', 
                'title': 'Seleccione la dependencia a la que pertenece'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Lic. Juan Pérez González',
                'autocomplete': 'name'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Director de Desarrollo Social'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select shadow-sm'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm',
                'min': 1,
                'placeholder': 'Ej. 1, 2, 3...'
            }),
            'numero_contacto': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. +52 (123) 456-7890',
                'pattern': r'[\d\s\+\(\)\-\.]+',
                'autocomplete': 'tel'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'ejemplo@gobierno.gob.mx',
                'autocomplete': 'email'
            }),
            'pagina_web': forms.URLInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'https://www.ejemplo.gob.mx',
                'autocomplete': 'url'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. (123) 456-7890',
                'pattern': r'[\d\s\+\(\)\-\.]+',
            }),
            'horario': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Lunes a Viernes 9:00 - 17:00'
            }),
            'semblanza': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 5,
                'placeholder': 'Breve descripción de la trayectoria profesional del funcionario...'
            }),
            'formacion_academica': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Detalle los estudios y certificaciones obtenidas...'
            }),
            'experiencia': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Detalle la experiencia laboral relevante...'
            }),
            'area': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Ej. Desarrollo Económico'
            }),
            'descripcion_area': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 4,
                'placeholder': 'Descripción de las funciones y responsabilidades del área...'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control shadow-sm',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar campos obligatorios
        required_fields = ['municipio', 'dependencia', 'nombre', 'cargo', 'status']
        for field_name in required_fields:
            self.fields[field_name].required = True
            if field_name in self.fields and 'class' in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['class'] += ' border-primary'
        
        # Campos opcionales pueden tener un estilo diferente
        for field_name, field in self.fields.items():
            if not field.required:
                field.label = f"{field.label} (Opcional)"


        
COMMON_FIELDS = [
    'municipio', 'dependencia', 'nombre', 'cargo', 'status', 'orden',
    'numero_contacto', 'correo_electronico', 'pagina_web',
    'telefono', 'horario', 'semblanza', 'formacion_academica',
    'experiencia', 'area', 'descripcion_area', 'imagen',
]

COMMON_LABELS = {
    'municipio': _('Municipio'),
    'dependencia': _('Dependencia'),
    'nombre': _('Nombre Completo'),
    'cargo': _('Cargo Oficial'),
    'status': _('Estado Actual'),
    'orden': _('Orden de Visualización'),
    'numero_contacto': _('Número de Contacto Directo'),
    'correo_electronico': _('Correo Electrónico Institucional'),
    'pagina_web': _('Sitio Web'),
    'telefono': _('Teléfono Oficina'),
    'horario': _('Horario de Atención'),
    'semblanza': _('Descripción Profesional'),
    'formacion_academica': _('Formación Académica'),
    'experiencia': _('Experiencia Profesional'),
    'area': _('Área de Responsabilidad'),
    'descripcion_area': _('Descripción del Área'),
    'imagen': _('Fotografía Oficial'),
}

COMMON_HELP_TEXTS = {
    'orden': _('Número que determina la posición en el listado (menor número = mayor prioridad)'),
    'numero_contacto': _('Formato recomendado: +52 (123) 456-7890'),
    'correo_electronico': _('Dirección de correo oficial para contacto público'),
    'imagen': _('Imagen profesional con fondo claro (tamaño recomendado: 400x600px)'),
    'semblanza': _('Descripción breve de la trayectoria profesional'),
}

COMMON_WIDGETS = {
    'municipio': forms.Select(attrs={
        'class': 'form-select shadow-sm',
        'data-bs-toggle': 'tooltip',
        'title': 'Seleccione el municipio correspondiente'
    }),
    'dependencia': forms.Select(attrs={
        'class': 'form-select shadow-sm',
        'data-bs-toggle': 'tooltip',
        'title': 'Seleccione la dependencia a la que pertenece'
    }),
    'nombre': forms.TextInput(attrs={
        'class': 'form-control shadow-sm',
        'placeholder': 'Ej. Lic. Juan Pérez González',
        'autocomplete': 'name'
    }),
    'cargo': forms.TextInput(attrs={
        'class': 'form-control shadow-sm',
        'placeholder': 'Ej. Director de Desarrollo Social'
    }),
    'status': forms.Select(attrs={'class': 'form-select shadow-sm'}),
    'orden': forms.NumberInput(attrs={
        'class': 'form-control shadow-sm',
        'min': 1,
        'placeholder': 'Ej. 1, 2, 3...'
    }),
    'numero_contacto': forms.TextInput(attrs={
        'class': 'form-control shadow-sm',
        'placeholder': 'Ej. +52 (123) 456-7890',
        'pattern': r'[\d\s\+\(\)\-\.]+',
        'autocomplete': 'tel'
    }),
    'correo_electronico': forms.EmailInput(attrs={
        'class': 'form-control shadow-sm',
        'placeholder': 'ejemplo@gobierno.gob.mx',
        'autocomplete': 'email'
    }),
    'pagina_web': forms.URLInput(attrs={
        'class': 'form-control shadow-sm',
        'placeholder': 'https://www.ejemplo.gob.mx',
        'autocomplete': 'url'
    }),
    'telefono': forms.TextInput(attrs={
        'class': 'form-control shadow-sm',
        'placeholder': 'Ej. (123) 456-7890',
        'pattern': r'[\d\s\+\(\)\-\.]+'
    }),
    'horario': forms.TextInput(attrs={
        'class': 'form-control shadow-sm',
        'placeholder': 'Ej. Lunes a Viernes 9:00 - 17:00'
    }),
    'semblanza': forms.Textarea(attrs={
        'class': 'form-control shadow-sm',
        'rows': 5,
        'placeholder': 'Breve descripción de la trayectoria profesional del funcionario...'
    }),
    'formacion_academica': forms.Textarea(attrs={
        'class': 'form-control shadow-sm',
        'rows': 4,
        'placeholder': 'Detalle los estudios y certificaciones obtenidas...'
    }),
    'experiencia': forms.Textarea(attrs={
        'class': 'form-control shadow-sm',
        'rows': 4,
        'placeholder': 'Detalle la experiencia laboral relevante...'
    }),
    'area': forms.TextInput(attrs={
        'class': 'form-control shadow-sm',
        'placeholder': 'Ej. Desarrollo Económico'
    }),
    'descripcion_area': forms.Textarea(attrs={
        'class': 'form-control shadow-sm',
        'rows': 4,
        'placeholder': 'Descripción de las funciones y responsabilidades del área...'
    }),
    'imagen': forms.ClearableFileInput(attrs={
        'class': 'form-control shadow-sm',
        'accept': 'image/*'
    }),
}


class BaseMiembroGabineteForm(forms.ModelForm):
    """
    Formulario base con configuración común para todos los modelos de miembros de gabinete.
    """
    class Meta:
        fields = COMMON_FIELDS
        labels = COMMON_LABELS
        help_texts = COMMON_HELP_TEXTS
        widgets = COMMON_WIDGETS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos obligatorios
        required_fields = ['municipio', 'dependencia', 'nombre', 'cargo', 'status']
        for fname in required_fields:
            field = self.fields.get(fname)
            if field:
                field.required = True
                field.widget.attrs['class'] += ' border-primary'
        # Marcar opcionales
        for fname, field in self.fields.items():
            if not field.required:
                field.label = f"{field.label} (Opcional)"



class MiembroGabinetePresidentesComuForm(BaseMiembroGabineteForm):
    class Meta(BaseMiembroGabineteForm.Meta):
        model = MiembroGabinetePresidentesComu


class MiembroGabineteCoordinadoresDifForm(BaseMiembroGabineteForm):
    class Meta(BaseMiembroGabineteForm.Meta):
        model = MiembroGabineteCoordinadoresDif