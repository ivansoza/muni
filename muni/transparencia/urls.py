from django.urls import path
from .views import HomeReportesView, HomeTransparenciaView, get_encuestas_activas, guardar_respuestas

urlpatterns = [
    path('', HomeTransparenciaView.as_view(), name='homeTransferencia'), 

    path('reportes/', HomeReportesView.as_view(), name='homeReportes'), 
    path('api/encuesta/activas/<int:municipio_id>/', get_encuestas_activas, name='get_encuestas_activas'),
    path('api/encuesta/enviar/', guardar_respuestas, name='guardar_respuestas'),
    
]