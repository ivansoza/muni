from django.urls import path
from .views import HomeTransparenciaView

urlpatterns = [
    path('', HomeTransparenciaView.as_view(), name='homeTransferencia'), 
]