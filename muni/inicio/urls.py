from django.urls import path
from .views import HomeInicioView

urlpatterns = [
    path('', HomeInicioView.as_view(), name='homeInicio'), 
]