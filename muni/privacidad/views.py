from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import AvisoDePrivacidad

class HomePrivacidad(TemplateView):
    template_name = 'homePrivacidad.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'transparencia'
        
        # Usar select_related para cargar los archivos relacionados de manera eficiente
        avisos = AvisoDePrivacidad.objects.all().order_by('fecha_creacion').prefetch_related('archivos_relacionados')
        
        context['avisos'] = avisos
        return context
 