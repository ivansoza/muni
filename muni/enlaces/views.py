from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeEnlacesView(TemplateView):
    template_name = 'homeEnlaces.html'  