from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeEventosView(TemplateView):
    template_name = 'homeEvents.html' 