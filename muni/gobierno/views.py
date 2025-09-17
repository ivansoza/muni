from django.shortcuts import render, redirect
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
from .forms import contenido_form_for
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_list_or_404

from django.db import transaction

class HomeGobiernoView(TemplateView):
    template_name = 'homeGobierno.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        municipio_activo = Municipio.objects.filter(status='activo').first()

        if municipio_activo:
            miembros_activos = municipio_activo.gabinete.filter(status='activo').order_by('orden')
            regidores_activos = municipio_activo.gabinete_regidores.filter(status='activo').order_by('orden')
            directores_activos = municipio_activo.gabinete_directores.filter(status='activo').order_by('orden')
            presidentes_comu_activos = municipio_activo.gabinete_presidentes_comu.filter(status='activo').order_by('orden')
            coordinadores_dif_activos = municipio_activo.gabinete_coordinadores_dif.filter(status='activo').order_by('orden')
        else:
            miembros_activos = None
            regidores_activos = None
            directores_activos = None
            presidentes_comu_activos = None
            coordinadores_dif_activos = None

        context.update({
            'municipio': municipio_activo,
            'miembros': miembros_activos,
            'regidores': regidores_activos,
            'directores': directores_activos,
            'presidentes_comu': presidentes_comu_activos,
            'coordinadores_dif': coordinadores_dif_activos,
            'sidebar': 'gobierno',
        })
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
                return modelo.objects.filter(
                    municipio=municipio_activo,
                    status='activo'
                ).count()
            return 0

        ctx['contacts_data'] = {
            'gabinete': contador(MiembroGabinete),
            'regidores': contador(MiembroGabineteRegidores),
            'directores': contador(MiembroGabineteDirectores),
            'presidentes_comu': contador(MiembroGabinetePresidentesComu),
            'coordinadores_dif': contador(MiembroGabineteCoordinadoresDif),
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
            'tiene_usuario': bool(m.usuario_id),
            'usuario': getattr(m.usuario, 'username', None) if m.usuario_id else None,
        } for m in qs
    ]})

User = get_user_model()

class AsociarUsuarioView(TemplateView):
    template_name = 'admin/asociar_usuario.html'

    MODEL_MAP = {
        'gabinete': MiembroGabinete,
        'regidor': MiembroGabineteRegidores,
        'director': MiembroGabineteDirectores,
        'presidente': MiembroGabinetePresidentesComu,
        'coordinador_dif': MiembroGabineteCoordinadoresDif,
    }

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tipo = self.kwargs['tipo']
        pk = self.kwargs['pk']
        model = self.MODEL_MAP.get(tipo)
        if not model:
            raise Http404("Tipo no válido")
        obj = get_object_or_404(model, pk=pk)
        ctx.update({
            'miembro': obj,
            'tipo': tipo,
            'assign_url': reverse('asignar_usuario_api', kwargs={'tipo': tipo, 'pk': pk}),
            'buscar_url': reverse('buscar_usuarios_api'),
            'breadcrumb': {
                'parent': {'name': 'Gabinete', 'url': reverse('dashboard')},
                'child':  {'name': 'Asociar usuario', 'url': ''},
            },
            'sidebar': 'gabinete',
        })
        return ctx


def _linked_info_for_user(user):
    """
    Devuelve (is_linked, label, url_perfil) si el user está ligado
    a alguno de los modelos; si no, (False, None, None).
    """
    # Busca en cada modelo si existe un registro con usuario=user
    pairings = [
        ('gabinete', MiembroGabinete, 'miembros_gabinete'),
        ('regidor', MiembroGabineteRegidores, 'miembros_regidores'),
        ('director', MiembroGabineteDirectores, 'miembros_directores'),
        ('presidente', MiembroGabinetePresidentesComu, 'miembros_presidentes_comu'),
        ('coordinador_dif', MiembroGabineteCoordinadoresDif, 'miembros_coordinadores_dif'),
    ]
    for tipo, Model, _rel in pairings:
        obj = Model.objects.filter(usuario=user).first()
        if obj:
            return True, f"{tipo}: {obj.nombre}", None
    return False, None, None


@login_required
def buscar_usuarios_api(request):
    """
    GET /api/usuarios/buscar/?q=texto&limit=20
    Devuelve dos listas: disponibles (no ligados) y ocupados (ya ligados).
    """
    q = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 20) or 20)

    qs = User.objects.all().order_by('username')
    if q:
        from django.db.models import Q
        qs = qs.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

    disponibles, ocupados = [], []
    for u in qs[:limit]:
        is_linked, label, _ = _linked_info_for_user(u)
        item = {
            'id': u.id,
            'username': u.username,
            'email': u.email or '',
            'full_name': f"{u.first_name} {u.last_name}".strip() or u.username,
            'is_linked': is_linked,
            'linked_label': label,
        }
        (ocupados if is_linked else disponibles).append(item)

    return JsonResponse({'disponibles': disponibles, 'ocupados': ocupados})


@login_required
@transaction.atomic
def asignar_usuario_api(request, tipo, pk):
    """
    POST: user_id -> asigna el usuario a este miembro.
    Si el usuario ya está ligado a otro miembro, se desliga del anterior.
    """
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

    MODEL_MAP = {
        'gabinete': MiembroGabinete,
        'regidor': MiembroGabineteRegidores,
        'director': MiembroGabineteDirectores,
        'presidente': MiembroGabinetePresidentesComu,
        'coordinador_dif': MiembroGabineteCoordinadoresDif,
    }
    Model = MODEL_MAP.get(tipo)
    if not Model:
        return JsonResponse({'ok': False, 'error': 'Tipo no válido'}, status=400)

    miembro = get_object_or_404(Model, pk=pk)
    user_id = request.POST.get('user_id')
    if not user_id:
        return JsonResponse({'ok': False, 'error': 'user_id requerido'}, status=400)

    user = get_object_or_404(User, pk=user_id)

    # Desligar al usuario si ya está ligado a otro miembro de cualquiera de los modelos
    pairings = [
        MiembroGabinete, MiembroGabineteRegidores, MiembroGabineteDirectores,
        MiembroGabinetePresidentesComu, MiembroGabineteCoordinadoresDif
    ]
    for M in pairings:
        prev = M.objects.filter(usuario=user).first()
        if prev and (prev.pk != miembro.pk or prev.__class__ != miembro.__class__):
            prev.usuario = None
            prev.save(update_fields=['usuario'])

    # Asignar al miembro actual
    miembro.usuario = user
    miembro.save(update_fields=['usuario'])

    return JsonResponse({'ok': True, 'message': 'Usuario asignado correctamente'})
    

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
        messages.success(self.request, "Presidente de comunidad creado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['breadcrumb'] = {
            'parent': {'name': 'Lista de Presidentes de Comunidad', 'url': '/gobierno/lista-presidentes-comu/'},
            'child': {'name': 'Crear Nuevo Presidente de Comunidad', 'url': ''}
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
        messages.success(self.request, "Presidente de Comunidad actualizado con éxito.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['breadcrumb'] = {
            'parent': {'name': 'Lista de Presidentes de Comunidad', 'url': '/gobierno/lista-presidentes-comu/'},
            'child': {'name': 'Editar Presidente de Comunidad', 'url': ''}
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
    
# Mapeo de 'tipo' -> (Modelo, etiqueta legible)
TIPO_MODELOS = {
    "gabinete": (MiembroGabinete, "Miembro principal"),
    "regidor": (MiembroGabineteRegidores, "Regidor/Regidora"),
    "director": (MiembroGabineteDirectores, "Director/Directora"),
    "presidente": (MiembroGabinetePresidentesComu, "Presidente de Comunidad"),
    "coordinador_dif": (MiembroGabineteCoordinadoresDif, "Coordinador(a) DIF"),
}

def _municipio_activo():
    return Municipio.objects.filter(status="activo").first()

from django.contrib.auth.decorators import login_required
from django.http import Http404
@login_required
def pre_editar_persona(request, tipo, pk):
    """
    Pre-editar: muestra el perfil y abajo un CKEditor para 'contenido'.
    Guarda en el mismo endpoint.
    """
    tipo_key = (tipo or "").lower().strip()
    if tipo_key not in TIPO_MODELOS:
        raise Http404("Tipo no válido.")

    Model, tipo_label = TIPO_MODELOS[tipo_key]

    municipio = _municipio_activo()
    if not municipio:
        raise Http404("No hay un municipio activo configurado.")

    persona = get_object_or_404(Model, pk=pk, municipio=municipio)

    # Form dinámico solo con 'contenido'
    Form = contenido_form_for(Model)

    if request.method == "POST":
        form = Form(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            messages.success(request, "Contenido actualizado correctamente.")
            # Redirige a la misma página para ver el contenido guardado
            return redirect("pre_editar_persona", tipo=tipo_key, pk=persona.pk)
    else:
        form = Form(instance=persona)
    url_configuracion = reverse("ListarGabineteView")

    ctx = {
        "persona": persona,
        "tipo": tipo_key,
        "tipo_label": tipo_label,
        "form": form,          
        "url_edicion": None,    
        "breadcrumb": {
            "parent": {"name": "Dashboard", "url": "/index"},
            "child":  {"name": "Lista de Miembros del Gabinete Presidencial", "url": ""},
        },
        "sidebar": "gabinete",
        "regreso_url": url_configuracion,

    }
    return render(request, "pre_editar_persona.html", ctx)


from django.urls import reverse, NoReverseMatch

def perfil_persona(request, tipo, pk):
    """
    Muestra el perfil público/único del miembro con su contenido (HTML)
    guardado con CKEditor. Si el usuario está autenticado, muestra botón
    para ir a editar (pre_editar_persona).
    """
    tipo_key = (tipo or "").strip().lower()
    if tipo_key not in TIPO_MODELOS:
        raise Http404("Tipo no válido.")

    Model, tipo_label = TIPO_MODELOS[tipo_key]

    municipio = _municipio_activo()
    if not municipio:
        raise Http404("No hay un municipio activo configurado.")

    persona = get_object_or_404(Model, pk=pk, municipio=municipio)

    # URL de regreso al directorio
    try:
        regreso_url = reverse("home_gobierno")
    except NoReverseMatch:
        # Fallback: usa tu ruta pública del directorio si es distinta
        regreso_url = "/gobierno/"

    ctx = {
        "persona": persona,
        "tipo": tipo_key,
        "tipo_label": tipo_label,
        "breadcrumb": {
            "parent": {"name": "Gobierno | Directorio", "url": regreso_url},
            "child":  {"name": persona.nombre, "url": ""},
        },
        "sidebar": "gobierno",
        "regreso_url": regreso_url,
        # Si está autenticado, mostramos un botón de edición
        "url_edicion": reverse("pre_editar_persona", args=[tipo_key, persona.pk]) if request.user.is_authenticated else None,
    }
    return render(request, "perfil_persona.html", ctx)