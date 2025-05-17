from django.urls import path
from .views import HomeReportesView, HomeTransparenciaView, ReporteAlcantarilladoView, ReporteAlumbradoPublicoView, ReporteBacheView, ReporteServicioAguaView, consulta_reporte_ajax, get_encuestas_activas, guardar_respuestas
from .views import HomeTransparenciaView, EjerciciosPorSeccionView, lista_obligaciones

urlpatterns = [
    path('', HomeTransparenciaView.as_view(), name='homeTransferencia'), 

    path('reportes/', HomeReportesView.as_view(), name='homeReportes'), 
    path('api/encuesta/activas/<int:municipio_id>/', get_encuestas_activas, name='get_encuestas_activas'),
    path('api/encuesta/enviar/', guardar_respuestas, name='guardar_respuestas'),
    
    path('transparencia/secciones/ejercicios/<int:seccion_id>/', EjerciciosPorSeccionView.as_view(), name='lista_ejercicios'),
    path('lista-transparencia/', lista_obligaciones, name='lista_transparencia'),





    path(
        'transparencia/agua/',
        ReporteServicioAguaView.as_view(),
        name='reporte-servicio-agua'
    ),    
    
    
    path('bache/', ReporteBacheView.as_view(), name='reportes_bache'),
    path('alcantarillado/', ReporteAlcantarilladoView.as_view(), name='reportes_alcantarillado'),
    path('alumbrado/', ReporteAlumbradoPublicoView.as_view(), name='reportes_alumbrado'),
    path(
        "ajax/consulta-reporte/",
        consulta_reporte_ajax,
        name="ajax_consulta_reporte",
    ),

]