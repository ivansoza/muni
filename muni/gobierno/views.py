from django.shortcuts import render
from django.views.generic.base import TemplateView

from informacion_municipal.models import Municipio

# Create your views here.
class HomeGobiernoView(TemplateView):
    template_name = 'homeGobierno.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 1. Obtenemos el primer municipio con status activo
        municipio_activo = Municipio.objects.filter(status='activo').first()

        # 2. Si hay municipio activo, obtenemos sus miembros activos y ordenados
        if municipio_activo:
            miembros_activos = municipio_activo.gabinete.filter(status='activo').order_by('orden')
        else:
            miembros_activos = None

        # 3. Agregamos al contexto
        context['municipio'] = municipio_activo
        context['miembros'] = miembros_activos
        context['sidebar'] = 'gobierno'  # Marcar 'Inicio' como activo

        return context
    
class SemblanzaHomeView(TemplateView):
    template_name = 'homeSemblanza.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context