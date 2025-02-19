from django.urls import path
from .views import HomeTransparenciaView, EjerciciosPorSeccionView

urlpatterns = [
    path('', HomeTransparenciaView.as_view(), name='homeTransferencia'), 
    path('transparencia/secciones/ejercicios/<int:seccion_id>/', EjerciciosPorSeccionView.as_view(), name='lista_ejercicios'),

]