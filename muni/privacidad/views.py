from django.shortcuts import render
from django.views.generic.base import TemplateView


class HomePrivacidad(TemplateView):
    template_name = 'homePrivacidad.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'mas'  
        return context