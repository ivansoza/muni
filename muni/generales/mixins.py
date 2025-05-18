# en tu app, por ejemplo en generals/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from reportes.models import (
    ReporteServicioAgua,
    ReporteBache,
    ReporteAlcantarillado,
    ReporteAlumbradoPublico,
)

class SuperuserOrReportPermissionMixin:
    """
    Permite el acceso si el usuario es superusuario,
    o si tiene ANY permiso (view/add/change) sobre alguno de los modelos de reporte.
    """
    report_models = [
        ReporteServicioAgua,
        ReporteBache,
        ReporteAlcantarillado,
        ReporteAlumbradoPublico,
    ]

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # 1) LoginRequiredMixin ya habrá redirigido a login si no está autenticado
        # 2) Si es superusuario, dejamos pasar
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # 3) Comprobamos permisos de modelo: view_*, add_* o change_*  
        for model in self.report_models:
            opts = model._meta
            for action in ('view', 'add', 'change'):
                perm = f"{opts.app_label}.{action}_{opts.model_name}"
                if user.has_perm(perm):
                    return super().dispatch(request, *args, **kwargs)

        # 4) Si no cumple ninguna condición, devolvemos 403
        raise PermissionDenied
