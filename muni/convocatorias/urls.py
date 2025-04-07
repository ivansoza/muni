from django.urls import path
from .views import HomeConvocatoriasView, detalleConvocatoria, filtrar_convocatorias

urlpatterns = [
    path('', HomeConvocatoriasView.as_view(), name='HomeConvocatoriasView'), 
    path('filtrar_convocatorias/', filtrar_convocatorias, name='filtrar_convocatorias'),
    path('detalleConvocatoria/<int:id>/', detalleConvocatoria.as_view(), name='detalleConvocatoria'),

]