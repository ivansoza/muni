from django.urls import path
from .views import HomeEnlacesView

urlpatterns = [
    path('', HomeEnlacesView.as_view(), name='homeEnlaces'), 
]