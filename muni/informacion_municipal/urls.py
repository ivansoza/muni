from django.urls import path

from generales.views import get_municipio_data
from .views import HomeInformacionView, guardar_colores

urlpatterns = [
    path('', HomeInformacionView.as_view(), name='homeInformacion'), 
    path('ajax/municipio/', get_municipio_data, name='ajax_municipio_data'),
    path('ajax/guardar-colores/', guardar_colores, name='guardar_colores'),

]