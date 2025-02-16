from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeTransparenciaView(TemplateView):
    template_name = 'homeTransparencia.html' 




class HomeReportesView(TemplateView):
    template_name = 'reportes/reportes.html' 