from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView

from generales.models import ContadorVisitas
from noticias.models import Noticia



class HomePageView(TemplateView):
    template_name = 'home/index.html'  # Ruta del template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'home'  # Marcar 'Inicio' como activo
        # Cargar las últimas 3 noticias ordenadas por fecha descendente
        context['ultimas_noticias'] = Noticia.objects.order_by('-fecha')[:3]


                # Manejo del contador de visitas
        if 'visita' not in self.request.session:
            self.request.session['visita'] = True  # Marcamos que la visita es real

            # Crear o actualizar el contador
            contador, created = ContadorVisitas.objects.get_or_create(id=1)
            contador.visitas += 1
            contador.save()


        return context

    
def mi_custom_error_400(request, exception):
    return render(request, 'errors/400.html', status=400)

def mi_custom_error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def mi_custom_error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def mi_custom_error_500(request):
    return render(request, 'errors/500.html', status=500)