# reportes/admin.py
from django.contrib import admin

from .models import (
    ReporteServicioAgua,
    ReporteBache,
    ReporteAlcantarillado,
    ReporteAlumbradoPublico, ReporteStatus
)

# Campos que mostraremos en todas las listas
_list_display = (
    "codigo_seguimiento",
    "nombre_solicitante",
    "estatus",
    "ubicacion",
    "creado",
)

_list_filter = ("estatus", "creado")
_search = ("codigo_seguimiento", "nombre_solicitante", "ubicacion", "descripcion")


class _BaseReporteAdmin(admin.ModelAdmin):  # noqa: D101  (solo uso interno)
    list_display = _list_display
    list_filter = _list_filter
    search_fields = _search
    readonly_fields = ("codigo_seguimiento", "creado", "actualizado")
    date_hierarchy = "creado"


admin.site.register(ReporteServicioAgua, _BaseReporteAdmin)
admin.site.register(ReporteBache, _BaseReporteAdmin)
admin.site.register(ReporteAlcantarillado, _BaseReporteAdmin)
admin.site.register(ReporteAlumbradoPublico, _BaseReporteAdmin)
admin.site.register(ReporteStatus)