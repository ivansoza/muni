from django.urls import path
from .views import HomeServiciosView, ServicioDetailView, ServicioDetalleParcialView, TramitesPorAreaView, requisito_adjunto_pdf_inline_view, requisito_pdf_inline_view

urlpatterns = [
    path('', HomeServiciosView.as_view(), name='homeServicios'), 
    path('area/<int:organismo_id>/', TramitesPorAreaView.as_view(), name='tramites_por_area'),
    path('pdf/requisito/<int:requisito_id>/', requisito_pdf_inline_view, name='requisito_pdf_inline'),
    path('pdf/requisito-adjunto/<int:adjunto_id>/', requisito_adjunto_pdf_inline_view, name='requisito_adjunto_pdf_inline'),
    path('<uuid:pk>/', ServicioDetailView.as_view(), name='detalle_servicio'),
    path('<uuid:pk>/detalle_parcial/', ServicioDetalleParcialView.as_view(), name='detalle_servicio_parcial'),
]