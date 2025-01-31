from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeTramitesView(TemplateView):
    template_name = 'homeTramites.html' 