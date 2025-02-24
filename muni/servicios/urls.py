from django.urls import path
from .views import HomeServiciosView, ServicioDetailView

urlpatterns = [
    path('', HomeServiciosView.as_view(), name='homeServicios'),  # Homepage
    path('<uuid:pk>/', ServicioDetailView.as_view(), name='detalle_servicio'),
]