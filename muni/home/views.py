from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = 'home/index.html'  # Ruta del template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'home'  # Marcar 'Inicio' como activo
        return context