from django import forms

from servicios.models import EnQueConsiste, Servicio

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
