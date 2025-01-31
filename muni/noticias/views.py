from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeNoticiasView(TemplateView):
    template_name = 'homeNoticias.html' 


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'noticias'  # Define qué opción está activa
        return context