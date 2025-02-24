from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeEventosView(TemplateView):
    template_name = 'homeEvents.html' 


class HomeHablaView(TemplateView):
    template_name = 'homeHabla.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'mas'  
        return context