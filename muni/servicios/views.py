from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeServiciosView(TemplateView):
    template_name = 'homeServicios.html'  # Ruta del template