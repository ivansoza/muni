from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeConvocatoriasView(TemplateView):
    template_name = 'homeConvocatorias.html'  


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'mas'  
        return context