from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeNoticiasView(TemplateView):
    template_name = 'homeNoticias.html' 