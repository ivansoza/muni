from django.views.generic import TemplateView
from .models import EdicionGaceta


class HomeGacetaView(TemplateView):
    template_name = 'homeGaceta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ediciones = EdicionGaceta.objects.filter(activo=True).order_by('-anio', '-fecha_publicacion')
        context['ediciones'] = ediciones
        context['ultima_edicion'] = ediciones.first()
        context['anios_disponibles'] = (
            ediciones.values_list('anio', flat=True).distinct().order_by('-anio')
        )
        context['total'] = ediciones.count()
        return context
