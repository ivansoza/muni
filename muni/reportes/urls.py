# reportes/urls.py
from django.urls import path

from .views import (
    ReporteAguaListView,
    ReporteBacheListView,
    ReporteAlcantarilladoListView,
    ReporteAlumbradoListView,
    reporte_status,
    toggle_reporte_status,
)


urlpatterns = [
    # AJAX endpoints
    path('status/<str:tipo>/', reporte_status, name='reporte-status'),
    path('status/<str:tipo>/toggle/', toggle_reporte_status, name='toggle-reporte-status'),

    path("agua/",           ReporteAguaListView.as_view(),          name="lista-agua"),
    path("bache/",          ReporteBacheListView.as_view(),         name="lista-bache"),
    path("alcantarillado/", ReporteAlcantarilladoListView.as_view(),name="lista-alcantarillado"),
    path("alumbrado/",      ReporteAlumbradoListView.as_view(),     name="lista-alumbrado"),
]