from django import forms

from servicios.models import ComoLoRealizo, CuantoCuesta, EnQueConsiste, QueSeRequiere, Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['titulo', 'descripcion', 'url_tramite', 'estado', 
                  'clasificacion', 'sector', 'organismo', 'pago_en_linea', 'ahora_en_linea', 'responsable']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3})
        }

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