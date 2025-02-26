from django import forms

from servicios.models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['titulo', 'descripcion', 'url_tramite', 'estado', 
                  'clasificacion', 'sector', 'organismo', 'pago_en_linea', 'ahora_en_linea']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3})
        }