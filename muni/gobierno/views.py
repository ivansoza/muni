from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeGobiernoView(TemplateView):
    template_name = 'homeGobierno.html' 