from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeServiciosView(TemplateView):
    template_name = 'homeServicios.html'  # Ruta del template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'servicios'  # Define qué opción está activa
        return context