from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse

# Create your views here.



class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'mi_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/admin'},
            'child': {'name': 'Mi Perfil', 'url': ''}
        }
        context['sidebar'] = 'Generales' 
        url_configuracion = reverse( 'dashboard')
        context['regreso_url']= url_configuracion
        context['usuario'] = self.request.user

        return context