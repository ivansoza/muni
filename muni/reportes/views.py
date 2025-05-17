# reportes/views.py
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from django.http import Http404
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.utils.translation import gettext_lazy as _

from reportes.forms import ReporteAdminForm
from reportes.models import (
    ReporteStatus,
    ReporteServicioAgua,
    ReporteBache,
    ReporteAlcantarillado,
    ReporteAlumbradoPublico,
)


# ─────────────────────────── Reportes de Agua ───────────────────────────
class ReporteAguaListView(LoginRequiredMixin, ListView):
    model = ReporteServicioAgua
    template_name = "reporte_list.html"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Reportes", "url": "/admin/generales/reportes"},
            "child": {"name": "Reportes de Agua", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse("ReportesView")

        reporte_status, _ = ReporteStatus.objects.get_or_create(
            pk=1,
            defaults={
                "reporte_agua_status": False,
                "reporte_bache_status": False,
                "reporte_alcantarillado_status": False,
                "reporte_alumbrado_status": False,
            },
        )
        context["reporte_status"] = reporte_status

        qs = self.get_queryset()
        context["total_reportes"]   = qs.count()
        context["total_resueltos"]  = qs.filter(estatus=self.model.Estatus.RESUELTO).count()
        context["total_pendientes"] = qs.filter(estatus=self.model.Estatus.PENDIENTE).count()

        # ← Aquí agregas la lista de toggles
        context["toggle_tipo"]  = "agua"
        context["toggle_label"] = "Agua"
        return context



# ─────────────────────────── Reportes de Bache ───────────────────────────
class ReporteBacheListView(LoginRequiredMixin, ListView):
    model = ReporteBache
    template_name = "reporte_list.html"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Reportes", "url": "/admin/generales/reportes"},
            "child": {"name": "Reportes de Baches", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse("ReportesView")

        reporte_status, _ = ReporteStatus.objects.get_or_create(pk=1, defaults={
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        })
        context["reporte_status"] = reporte_status

        qs = self.get_queryset()
        context["toggle_tipo"]  = "bache"
        context["toggle_label"] = "Baches"
        context["total_reportes"]   = qs.count()
        context["total_resueltos"]  = qs.filter(estatus=self.model.Estatus.RESUELTO).count()
        context["total_pendientes"] = qs.filter(estatus=self.model.Estatus.PENDIENTE).count()
        return context


# ──────────────────────── Reportes de Alcantarillado ────────────────────────
class ReporteAlcantarilladoListView(LoginRequiredMixin, ListView):
    model = ReporteAlcantarillado
    template_name = "reporte_list.html"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Reportes", "url": "/admin/generales/reportes"},
            "child": {"name": "Reportes de Alcantarillado", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse("ReportesView")

        reporte_status, _ = ReporteStatus.objects.get_or_create(pk=1, defaults={
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        })
        context["reporte_status"] = reporte_status
        context["toggle_tipo"]  = "alcantarillado"
        context["toggle_label"] = "Alcantarillado"
        qs = self.get_queryset()
        context["total_reportes"]   = qs.count()
        context["total_resueltos"]  = qs.filter(estatus=self.model.Estatus.RESUELTO).count()
        context["total_pendientes"] = qs.filter(estatus=self.model.Estatus.PENDIENTE).count()
        return context


# ─────────────────────── Reportes de Alumbrado Público ──────────────────────
class ReporteAlumbradoListView(LoginRequiredMixin, ListView):
    model = ReporteAlumbradoPublico
    template_name = "reporte_list.html"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Reportes", "url": "/admin/generales/reportes"},
            "child": {"name": "Reportes de Alumbrado Público", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse("ReportesView")

        reporte_status, _ = ReporteStatus.objects.get_or_create(pk=1, defaults={
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        })
        context["reporte_status"] = reporte_status
        context["toggle_tipo"]  = "alumbrado"
        context["toggle_label"] = "Alumbrado"
        qs = self.get_queryset()
        context["total_reportes"]   = qs.count()
        context["total_resueltos"]  = qs.filter(estatus=self.model.Estatus.RESUELTO).count()
        context["total_pendientes"] = qs.filter(estatus=self.model.Estatus.PENDIENTE).count()
        return context




# Lista de tipos válidos
VALID_REPORTES = {
    'agua': 'reporte_agua_status',
    'bache': 'reporte_bache_status',
    'alcantarillado': 'reporte_alcantarillado_status',
    'alumbrado': 'reporte_alumbrado_status',
}
@login_required
def reporte_status(request, tipo):
    """
    GET: devuelve {"status": true|false} para el campo correspondiente.
    """
    if tipo not in VALID_REPORTES:
        return HttpResponseBadRequest('Tipo de reporte inválido.')
    campo = VALID_REPORTES[tipo]
    obj, _ = ReporteStatus.objects.get_or_create(
        pk=1,
        defaults={c: False for c in VALID_REPORTES.values()}
    )
    return JsonResponse({'status': getattr(obj, campo)})

@login_required
@require_POST
def toggle_reporte_status(request, tipo):
    """
    POST: {"status": true|false} → actualiza el campo y devuelve el nuevo estado.
    """
    if tipo not in VALID_REPORTES:
        return HttpResponseBadRequest('Tipo de reporte inválido.')
    try:
        data = json.loads(request.body)
        nuevo = bool(data.get('status'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Payload inválido.')
    campo = VALID_REPORTES[tipo]
    obj, _ = ReporteStatus.objects.get_or_create(
        pk=1,
        defaults={c: False for c in VALID_REPORTES.values()}
    )
    setattr(obj, campo, nuevo)
    obj.save(update_fields=[campo])
    return JsonResponse({'status': getattr(obj, campo)})


# views.py  (añade / ajusta lo siguiente)

class ReporteDetailView(LoginRequiredMixin, UpdateView):
    """
    Muestra y permite actualizar estatus / comentarios de cualquier reporte.
    Las actualizaciones se reciben vía POST (AJAX → JSON).
    """
    template_name = "reporte_detail.html"
    form_class    = ReporteAdminForm   # se adaptará dinámicamente al modelo

    _MODEL_MAP = {                     # ← como antes
        "agua":           ReporteServicioAgua,
        "bache":          ReporteBache,
        "alcantarillado": ReporteAlcantarillado,
        "alumbrado":      ReporteAlumbradoPublico,
    }
    _LIST_URL_NAME_MAP = {
        "agua":           "lista-agua",
        "bache":          "lista-bache",
        "alcantarillado": "lista-alcantarillado",
        "alumbrado":      "lista-alumbrado",
    }

    # ------- dispatch ----------------------------------------------------------
    def dispatch(self, request, *args, **kwargs):
        tipo = kwargs.get("tipo")
        try:
            self.model        = self._MODEL_MAP[tipo]
            self.tipo         = tipo
            self._list_url    = self._LIST_URL_NAME_MAP[tipo]
            self.object       = self.get_object()          # evita doble consulta
            # Ajusta el ModelForm al modelo correcto
            self.form_class.Meta.model = self.model
        except KeyError:
            raise Http404(_("Tipo de reporte no válido"))
        return super().dispatch(request, *args, **kwargs)

    # ------- contexto ----------------------------------------------------------
# views.py  (sólo cambia get_context_data)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.object

        gmaps_url = ""
        if obj.latitud and obj.longitud:
            gmaps_url = f"https://www.google.com/maps?q={obj.latitud},{obj.longitud}"

        ctx |= {
            "breadcrumb": {
                "parent": {"name": "Reportes", "url": reverse("ReportesView")},
                "child":  {"name": f"Reporte {self.tipo.title()}", "url": ""},
            },
            "sidebar":      "Generales",
            "regreso_url":  reverse(self._list_url),
            "comentarios":  obj.comentarios or _("Sin comentarios"),
            "gmaps_url":    gmaps_url,
        }
        return ctx

    # ------- manejo POST (AJAX) -----------------------------------------------
    def form_invalid(self, form):
        """Errores → JSON status 400, para mostrar en SweetAlert."""
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    def form_valid(self, form):
        form.save()
        return JsonResponse({
            "ok":        True,
            "message":   _("Cambios guardados correctamente"),
            "estatus":   self.object.get_estatus_display(),
            "comentarios": self.object.comentarios or ("Sin comentarios"),
        })