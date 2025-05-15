# reportes/urls.py
from django.urls import path

from .views import (
    ReporteAguaListView,
    ReporteBacheListView,
    ReporteAlcantarilladoListView,
    ReporteAlumbradoListView,
)


urlpatterns = [
    path("agua/",           ReporteAguaListView.as_view(),          name="lista-agua"),
    path("bache/",          ReporteBacheListView.as_view(),         name="lista-bache"),
    path("alcantarillado/", ReporteAlcantarilladoListView.as_view(),name="lista-alcantarillado"),
    path("alumbrado/",      ReporteAlumbradoListView.as_view(),     name="lista-alumbrado"),
]