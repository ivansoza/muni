# reportes/views.py
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

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