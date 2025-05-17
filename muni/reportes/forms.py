# forms.py
from django import forms
from .models import (
    ReporteServicioAgua, ReporteBache,
    ReporteAlcantarillado, ReporteAlumbradoPublico
)

class ReporteAdminForm(forms.ModelForm):
    class Meta:
        # el modelo real se inyecta dinámicamente en la vista
        model   = ReporteServicioAgua
        fields  = ("estatus", "comentarios")
        widgets = {
            "estatus": forms.Select(
                attrs={"class": "form-select", "required": True}
            ),
            "comentarios": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Comentarios internos…"}
            ),
        }
