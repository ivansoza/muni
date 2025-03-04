
from django.shortcuts import render
from .models import Carpeta, Archivo
from django.views.generic import TemplateView
class HomeSevacView(TemplateView):
    template_name = 'archivosListas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener las carpetas principales activas
        carpetas = Carpeta.objects.filter(padre=None, estatus='A')

        # Añadir las carpetas activas al contexto
        context['carpetas'] = carpetas
        return context
