from django.urls import path
from .views import HomeConvocatoriasView

urlpatterns = [
    path('', HomeConvocatoriasView.as_view(), name='HomeConvocatoriasView'), 
]