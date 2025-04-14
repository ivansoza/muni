from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView

from generales.models import ContadorVisitas
from noticias.models import Noticia
from convocatorias.models import Convocatoria
from django.core.exceptions import ObjectDoesNotExist


class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'home'
        context['ultimas_noticias'] = Noticia.objects.order_by('-fecha')[:3]

        # Agregar convocatorias (las 5 más recientes abiertas o próximas)
        context['convocatorias'] = Convocatoria.objects.filter(
            estado__in=['ABIERTA', 'PRÓXIMA']
        ).order_by('-fecha_apertura')[:5]

        if 'visita' not in self.request.session:
            self.request.session['visita'] = True
            contador, _ = ContadorVisitas.objects.get_or_create(id=1)
            contador.visitas += 1
            contador.save()
        try:
            # Intentar obtener el contador de visitas
            contador = ContadorVisitas.objects.get(id=1)
            context['contador_visitas'] = contador.visitas
        except ObjectDoesNotExist:
            # Si no existe, asignamos 0 como valor por defecto
            context['contador_visitas'] = 0

        return context

    
def mi_custom_error_400(request, exception):
    return render(request, 'errors/400.html', status=400)

def mi_custom_error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def mi_custom_error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def mi_custom_error_500(request):
    return render(request, 'errors/500.html', status=500)