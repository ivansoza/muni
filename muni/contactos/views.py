from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeContactsView(TemplateView):
    template_name = 'homeContact.html' 