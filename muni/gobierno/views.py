from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib import messages

from informacion_municipal.models import Municipio
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from gobierno.models import MiembroGabinete, MiembroGabineteCoordinadoresDif, MiembroGabineteDirectores, MiembroGabinetePresidentesComu, MiembroGabineteRegidores
from gobierno.forms import MiembroGabineteCoordinadoresDifForm, MiembroGabineteDirectorForm, MiembroGabineteForm, MiembroGabinetePresidentesComuForm, MiembroGabineteRegidorForm
# Create your views here.
# 
from django.shortcuts import get_list_or_404

from django.db import transaction

class HomeGobiernoView(TemplateView):
    template_name = 'homeGobierno.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 1. Obtenemos el primer municipio con status activo
        municipio_activo = Municipio.objects.filter(status='activo').first()

        # 2. Si hay municipio activo, obtenemos sus miembros activos y ordenados
        if municipio_activo:
            miembros_activos = municipio_activo.gabinete.filter(status='activo').order_by('orden')
            regidores_activos = municipio_activo.gabinete_regidores.filter(status='activo').order_by('orden')
            directores_activos = municipio_activo.gabinete_directores.filter(status='activo').order_by('orden')
        else:
            miembros_activos = None
            regidores_activos = None
            directores_activos = None

        # 3. Agregamos los datos al contexto
        context['municipio'] = municipio_activo
        context['miembros'] = miembros_activos
        context['regidores'] = regidores_activos
        context['directores'] = directores_activos
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
        ctx = super().get_context_data(**kwargs)

        ctx["breadcrumb"] = {
            'parent': {'name': 'Dashboard', 'url': '/index'},
            'child': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': ''}
        }
        ctx['sidebar'] = 'gabinete'

        municipio_activo = Municipio.objects.filter(status='activo').first()

        def contador(modelo):
            if municipio_activo:
                return modelo.objects.filter(municipio=municipio_activo,
                                             status='activo').count()
            return 0

        ctx['contacts_data'] = {
            'gabinete': contador(MiembroGabinete),
            'regidores': contador(MiembroGabineteRegidores),
            'directores': contador(MiembroGabineteDirectores),
        }

        ctx['regreso_url'] = reverse("dashboard")
        return ctx
    

def lista_miembros(request, modelo):
    municipio_activo = Municipio.objects.filter(status='activo').first()
    if municipio_activo:
        qs = modelo.objects.filter(municipio=municipio_activo).order_by('orden')
    else:
        qs = modelo.objects.none()

    return JsonResponse({'miembros': [
        {
            'id': m.id,
            'nombre': m.nombre,
            'cargo': m.cargo,
            'area': getattr(m, 'area', '') or '',
            'orden': m.orden,
            'status': 'Activo' if m.status == 'activo' else 'Inactivo',
        } for m in qs
    ]})

def gabinete_list_api(request):
    return lista_miembros(request, MiembroGabinete)


def regidores_list_api(request):
    return lista_miembros(request, MiembroGabineteRegidores)

def directores_list_api(request):
    return lista_miembros(request, MiembroGabineteDirectores)


def presidentes_comu_list_api(request):
    """
    Devuelve en JSON la lista de Presidentes Comunales
    activos en el municipio activo, ordenados por 'orden'.
    """
    return lista_miembros(request, MiembroGabinetePresidentesComu)


def coordinadores_dif_list_api(request):
    """
    Devuelve en JSON la lista de Coordinadores DIF
    activos en el municipio activo, ordenados por 'orden'.
    """
    return lista_miembros(request, MiembroGabineteCoordinadoresDif)


@require_POST
@csrf_exempt          # deja esta línea solo si no envías el header X‑CSRFTOKEN desde JS
def update_order(request, modelo):
    """
    Actualiza el campo 'orden' de cualquier modelo de gabinete
    (Gabinete, Regidores, Directores) **solo** para el primer
    municipio activo encontrado.
    """
    order_ids = request.POST.getlist('order[]')
    if not order_ids:
        return HttpResponseBadRequest('Sin datos de orden')

    municipio_activo = Municipio.objects.filter(status='activo').first()
    if not municipio_activo:
        return JsonResponse({'error': 'No existe municipio activo'}, status=400)

    # Traemos de golpe todos los objetos válidos y los metemos en un dict para O(1)
    miembros = get_list_or_404(
        modelo,
        id__in=order_ids,
        municipio=municipio_activo
    )
    miembros_map = {str(m.id): m for m in miembros}

    # Ajustamos el orden en memoria
    for idx, pk in enumerate(order_ids, start=1):
        if pk in miembros_map:     # ignoramos IDs que no pertenezcan al municipio activo
            miembros_map[pk].orden = idx

    # Guardamos en un solo golpe
    with transaction.atomic():
        modelo.objects.bulk_update(miembros, ['orden'])

    return JsonResponse({'message': 'Orden actualizado exitosamente'})


def gabinete_update_order_api(request):
    return update_order(request, MiembroGabinete)

def regidores_update_order_api(request):
    return update_order(request, MiembroGabineteRegidores)

def directores_update_order_api(request):
    return update_order(request, MiembroGabineteDirectores)

def presidentes_comu_update_order_api(request):
    """
    Wrapper para actualizar el orden de Presidentes Comunales.
    """
    return update_order(request, MiembroGabinetePresidentesComu)


def coordinadores_dif_update_order_api(request):
    """
    Wrapper para actualizar el orden de Coordinadores DIF.
    """
    return update_order(request, MiembroGabineteCoordinadoresDif)


class MiembroGabineteCreateView(LoginRequiredMixin, CreateView):
    model = MiembroGabinete
    form_class = MiembroGabineteForm
    template_name = 'admin/gabinete_form.html'
    success_url = reverse_lazy('ListarGabineteView')  # Ajusta al nombre de URL que desees

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Miembro principal creado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': '/gobierno/lista-gabinete/'},
            'child': {'name': 'Crear Nuevo Miembro', 'url': ''}
        }
        context['sidebar'] = 'gabinete'
        return context


class MiembroGabineteUpdateView(LoginRequiredMixin, UpdateView):
    model = MiembroGabinete
    form_class = MiembroGabineteForm
    template_name = 'admin/gabinete_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Miembro principal actualizado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': '/gobierno/lista-gabinete/'},
            'child': {'name': 'Editar Miembro', 'url': ''}
        }
        context['sidebar'] = 'gabinete'
        return context
    
class RegidorCreateView(LoginRequiredMixin, CreateView):
    model = MiembroGabineteRegidores
    form_class = MiembroGabineteRegidorForm
    template_name = 'admin/regidor_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Regidor creado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': '/gobierno/lista-gabinete/'},
            'child': {'name': 'Crear Nuevo Miembro', 'url': ''}
        }
        context['sidebar'] = 'gabinete'
        return context


class RegidorUpdateView(LoginRequiredMixin, UpdateView):
    model = MiembroGabineteRegidores
    form_class = MiembroGabineteRegidorForm
    template_name = 'admin/regidor_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Regidor actualizado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': '/gobierno/lista-gabinete/'},
            'child': {'name': 'Editar Miembro', 'url': ''}
        }
        context['sidebar'] = 'gabinete'
        return context
    

class DirectorCreateView(LoginRequiredMixin, CreateView):
    model = MiembroGabineteDirectores
    form_class = MiembroGabineteDirectorForm
    template_name = 'admin/directores_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Director creado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': '/gobierno/lista-gabinete/'},
            'child': {'name': 'Crear Nuevo Miembro', 'url': ''}
        }
        context['sidebar'] = 'gabinete'
        return context


class DirectorUpdateView(LoginRequiredMixin, UpdateView):
    model = MiembroGabineteDirectores
    form_class = MiembroGabineteDirectorForm
    template_name = 'admin/directores_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Director actualizado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            'parent': {'name': 'Lista de Miembros del Gabinete Presidencial', 'url': '/gobierno/lista-gabinete/'},
            'child': {'name': 'Editar Miembro', 'url': ''}
        }
        context['sidebar'] = 'gabinete'
        return context
    




class PresidenteComuCreateView(LoginRequiredMixin, CreateView):
    model = MiembroGabinetePresidentesComu
    form_class = MiembroGabinetePresidentesComuForm
    template_name = 'admin/presidentes_comu_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Presidente comunal creado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['breadcrumb'] = {
            'parent': {'name': 'Lista de Presidentes Comunales', 'url': '/gobierno/lista-presidentes-comu/'},
            'child': {'name': 'Crear Nuevo Presidente Comunal', 'url': ''}
        }
        ctx['sidebar'] = 'gabinete'
        return ctx


class PresidenteComuUpdateView(LoginRequiredMixin, UpdateView):
    model = MiembroGabinetePresidentesComu
    form_class = MiembroGabinetePresidentesComuForm
    template_name = 'admin/presidentes_comu_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Presidente comunal actualizado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['breadcrumb'] = {
            'parent': {'name': 'Lista de Presidentes Comunales', 'url': '/gobierno/lista-presidentes-comu/'},
            'child': {'name': 'Editar Presidente Comunal', 'url': ''}
        }
        ctx['sidebar'] = 'gabinete'
        return ctx


class CoordinadorDifCreateView(LoginRequiredMixin, CreateView):
    model = MiembroGabineteCoordinadoresDif
    form_class = MiembroGabineteCoordinadoresDifForm
    template_name = 'admin/coordinadores_dif_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Coordinador DIF creado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['breadcrumb'] = {
            'parent': {'name': 'Lista de Coordinadores DIF', 'url': '/gobierno/lista-coordinadores-dif/'},
            'child': {'name': 'Crear Nuevo Coordinador DIF', 'url': ''}
        }
        ctx['sidebar'] = 'gabinete'
        return ctx


class CoordinadorDifUpdateView(LoginRequiredMixin, UpdateView):
    model = MiembroGabineteCoordinadoresDif
    form_class = MiembroGabineteCoordinadoresDifForm
    template_name = 'admin/coordinadores_dif_form.html'
    success_url = reverse_lazy('ListarGabineteView')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Coordinador DIF actualizado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['breadcrumb'] = {
            'parent': {'name': 'Lista de Coordinadores DIF', 'url': '/gobierno/lista-coordinadores-dif/'},
            'child': {'name': 'Editar Coordinador DIF', 'url': ''}
        }
        ctx['sidebar'] = 'gabinete'
        return ctx