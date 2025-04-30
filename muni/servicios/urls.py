from django.urls import path
from .views import HomeServiciosView, ServicioDetailView, ServicioDetalleParcialView

urlpatterns = [
    path('', HomeServiciosView.as_view(), name='homeServicios'), 
    path('<uuid:pk>/', ServicioDetailView.as_view(), name='detalle_servicio'),
    path('<uuid:pk>/detalle_parcial/', ServicioDetalleParcialView.as_view(), name='detalle_servicio_parcial'),
]