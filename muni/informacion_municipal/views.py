from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeInformacionView(TemplateView):
    template_name = 'homeInfoMuni.html' 