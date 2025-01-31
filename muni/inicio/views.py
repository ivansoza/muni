from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeInicioView(TemplateView):
    template_name = 'homeInicio.html' 