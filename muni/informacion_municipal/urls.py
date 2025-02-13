from django.urls import path

from generales.views import get_municipio_data
from .views import HomeInformacionView

urlpatterns = [
    path('', HomeInformacionView.as_view(), name='homeInformacion'), 
    path('ajax/municipio/', get_municipio_data, name='ajax_municipio_data'),

]