from django.urls import path
from .views import HomeConvocatoriasView, detalleConvocatoria, filtrar_convocatorias, filtrar_convocatorias_seccion_plus

urlpatterns = [
    path('', HomeConvocatoriasView.as_view(), name='HomeConvocatoriasView'), 
    path('filtrar_convocatorias/', filtrar_convocatorias, name='filtrar_convocatorias'),
    path('detalleConvocatoria/<int:id>/', detalleConvocatoria.as_view(), name='detalleConvocatoria'),
    path(
        "seccion/<int:seccion_id>/detalleConvocatoria/<int:id>/",
        detalleConvocatoria.as_view(),
        name="detalleConvocatoria_desde_seccion",
    ),


    path('filtrar_convocatorias_seccion/<int:seccion_pk>/', filtrar_convocatorias_seccion_plus, name='filtrar_convocatorias_seccion_plus'),


    

]