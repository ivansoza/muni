from django import forms

from servicios.models import ComoLoRealizo, CuantoCuesta, EnQueConsiste, QueSeRequiere, RequisitosImagen, Servicio

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

        # Solo al campo 'organismo'
        self.fields['organismo'].widget.attrs.update({'class': 'form-control'})

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