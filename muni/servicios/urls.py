from django.urls import path
from .views import HomeServiciosView

urlpatterns = [
    path('', HomeServiciosView.as_view(), name='homeServicios'),  # Homepage
]