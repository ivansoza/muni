# reportes/views.py
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

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
    template_name = "reporte_list.html"       # usa la misma plantilla
    paginate_by = 25                                    # 25 por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = {
            "parent": {"name": "Reportes", "url": "/admin/generales/reportes"},
            "child": {"name": "Reportes de Agua", "url": ""},
        }
        context["sidebar"] = "Generales"
        context["regreso_url"] = reverse("generalesDashboard")

        reporte_status, _ = ReporteStatus.objects.get_or_create(pk=1, defaults={
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        })
        context["reporte_status"] = reporte_status

        qs = self.get_queryset()
        context["total_reportes"]     = qs.count()
        context["total_resueltos"]    = qs.filter(estatus=self.model.Estatus.RESUELTO).count()
        context["total_pendientes"]   = qs.filter(estatus=self.model.Estatus.PENDIENTE).count()
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
        context["regreso_url"] = reverse("generalesDashboard")

        reporte_status, _ = ReporteStatus.objects.get_or_create(pk=1, defaults={
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        })
        context["reporte_status"] = reporte_status

        qs = self.get_queryset()
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
        context["regreso_url"] = reverse("generalesDashboard")

        reporte_status, _ = ReporteStatus.objects.get_or_create(pk=1, defaults={
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        })
        context["reporte_status"] = reporte_status

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
        context["regreso_url"] = reverse("generalesDashboard")

        reporte_status, _ = ReporteStatus.objects.get_or_create(pk=1, defaults={
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        })
        context["reporte_status"] = reporte_status

        qs = self.get_queryset()
        context["total_reportes"]   = qs.count()
        context["total_resueltos"]  = qs.filter(estatus=self.model.Estatus.RESUELTO).count()
        context["total_pendientes"] = qs.filter(estatus=self.model.Estatus.PENDIENTE).count()
        return context
