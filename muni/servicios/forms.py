from django import forms

from servicios.models import ComoLoRealizo, ConfiguracionServicio, CuantoCuesta, EnQueConsiste, QueSeRequiere, RequisitoAdjunto, RequisitosImagen, Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['titulo', 'descripcion',
                  'clasificacion', 'sector', 'organismo', 'pago_en_linea', 'ahora_en_linea', 'responsable']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        config = ConfiguracionServicio.objects.first()
        self.is_v3 = bool(config and config.plantilla_home_version == 3)

        if self.is_v3:
            campos_v3 = {'titulo', 'descripcion', 'organismo'}
            for nombre in list(self.fields.keys()):
                if nombre not in campos_v3:
                    self.fields.pop(nombre, None)

            if 'descripcion' in self.fields:
                self.fields['descripcion'].required = False
                self.fields['descripcion'].help_text = 'Opcional'
                self.fields['descripcion'].widget.attrs.update({'placeholder': 'Opcional'})

            if 'organismo' in self.fields:
                self.fields['organismo'].label = 'Área'

        # Solo al campo 'organismo'
        if 'organismo' in self.fields:
            self.fields['organismo'].widget.attrs.update({'class': 'form-control'})

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '')
        if getattr(self, 'is_v3', False) and not descripcion:
            return 'N/A'
        return descripcion

class EnQueConsisteForm(forms.ModelForm):
    class Meta:
        model = EnQueConsiste
        fields = ['tramite', 'canal_presentacion', 'solicitado_por', 'momento_solicitud']

class QueSeRequiereForm(forms.ModelForm):
    class Meta:
        model = QueSeRequiere
        exclude = ['servicio']  
        widgets = {
            'especificaciones': forms.Textarea(attrs={'rows': 3}),
            'tipo_documento': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        hide_archivo = kwargs.pop('hide_archivo', False)
        super().__init__(*args, **kwargs)
        if hide_archivo:
            campos_v3 = {'nombre', 'especificaciones'}
            for nombre in list(self.fields.keys()):
                if nombre not in campos_v3:
                    self.fields.pop(nombre, None)

            self.fields['especificaciones'].required = False
            self.fields.pop('archivo_descarga', None)

class RequisitoAdjuntoForm(forms.ModelForm):
    class Meta:
        model = RequisitoAdjunto
        fields = ['archivo']

class RequisitosImagenForm(forms.ModelForm):
    class Meta:
        model = RequisitosImagen
        fields = ['imagen', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }


class ComoLoRealizoForm(forms.ModelForm):
    class Meta:
        model = ComoLoRealizo
        exclude = ['servicio']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3})
        }

class CuantoCuestaForm(forms.ModelForm):
    class Meta:
        model = CuantoCuesta
        exclude = ['servicio']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3})
        }