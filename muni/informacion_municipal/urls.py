from django.urls import path
from .views import HomeInformacionView

urlpatterns = [
    path('', HomeInformacionView.as_view(), name='homeInformacion'), 
]