from django.urls import path
from .views import HomeReportesView, HomeTransparenciaView

urlpatterns = [
    path('', HomeTransparenciaView.as_view(), name='homeTransferencia'), 

    path('reportes/', HomeReportesView.as_view(), name='homeReportes'), 


    
]