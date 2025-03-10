from django.shortcuts import render
from django.views.generic.base import TemplateView

from informacion_municipal.models import Municipio
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from gobierno.models import MiembroGabinete
from gobierno.forms import MiembroGabineteForm
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
    
class ListarGabineteView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/listGabinete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': ''}
        }
        context['sidebar'] = 'gabinete'  # Resalta la sección correspondiente

        # Obtenemos el primer municipio con status "activo"
        municipio_activo = Municipio.objects.filter(status='activo').first()
        
        # Si se encuentra un municipio activo, se cuentan los miembros activos asociados a él
        if municipio_activo:
            contador = MiembroGabinete.objects.filter(
                municipio=municipio_activo,
                status='activo'
            ).count()
        else:
            contador = 0

        # Se añade el contador al contexto en "contacts_data"
        context['contacts_data'] = {
            'contador_miembros_activos': contador
        }
        
        return context
    

def gabinete_list_api(request):
    """
    Devuelve la lista de miembros del gabinete en formato JSON,
    filtrados por el primer municipio activo encontrado y ordenados por el campo 'orden'.
    """
    if request.method == 'GET':
        # Obtenemos el primer municipio activo
        municipio_activo = Municipio.objects.filter(status='activo').first()
        if municipio_activo:
            # Filtramos los miembros del gabinete para el municipio activo
            miembros = MiembroGabinete.objects.filter(municipio=municipio_activo).order_by('orden')
        else:
            miembros = MiembroGabinete.objects.none()  # No hay municipio activo
        
        data = []
        for m in miembros:
            data.append({
                'id': m.id,
                'nombre': m.nombre,
                'cargo': m.cargo,
                'area': m.area if m.area else "",
                'orden': m.orden,
                'status': m.status,
            })
        return JsonResponse({'miembros': data}, safe=False)

    # Si no es método GET, responder con error
    return JsonResponse({'error': 'Método no permitido o no es AJAX'}, status=400)


@csrf_exempt  # Si manejas CSRF manualmente en AJAX, querrás usar esto o ajustar la configuración
def gabinete_update_order_api(request):
    """
    Actualiza el orden de los MiembroGabinete basado en la lista enviada por AJAX,
    pero únicamente para los miembros que pertenezcan al primer municipio activo.
    """
    if request.method == 'POST':
        # Obtenemos el primer municipio con status "activo"
        municipio_activo = Municipio.objects.filter(status='activo').first()
        if not municipio_activo:
            return JsonResponse({'error': 'No existe municipio activo'}, status=400)

        # 'order[]' llegará como lista con IDs en el orden deseado
        order_data = request.POST.getlist('order[]')

        for index, miembro_id in enumerate(order_data, start=1):
            # Se fuerza que el miembro pertenezca al municipio activo
            miembro = get_object_or_404(MiembroGabinete, id=miembro_id, municipio=municipio_activo)
            miembro.orden = index
            miembro.save()

        return JsonResponse({'message': 'Orden actualizado exitosamente'})

    return JsonResponse({'error': 'Método no permitido o no es AJAX'}, status=400)


class MiembroGabineteCreateView(LoginRequiredMixin,CreateView):
    model = MiembroGabinete
    form_class = MiembroGabineteForm
    template_name = 'admin/gabinete_form.html'
    success_url = reverse_lazy('ListarGabineteView')  # Ajusta al nombre de URL que desees

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': '/gobierno/lista-gabinete/'},
            'child': {'name': 'Crear Nuevo Miembro', 'url': ''}
        }
        context['sidebar'] = 'gabinete'  # Asegura que el sidebar resalte la sección de Transparencia
        return context
class MiembroGabineteUpdateView(LoginRequiredMixin,UpdateView):
    model = MiembroGabinete
    form_class = MiembroGabineteForm
    template_name = 'admin/gabinete_form.html'
    success_url = reverse_lazy('ListarGabineteView') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': '/gobierno/lista-gabinete/'},
            'child': {'name': 'Editar Nuevo Miembro', 'url': ''}
        }
        context['sidebar'] = 'gabinete'  # Asegura que el sidebar resalte la sección de Transparencia
        return context