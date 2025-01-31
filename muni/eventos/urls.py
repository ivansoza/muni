from django.urls import path
from .views import HomeEventosView

urlpatterns = [
    path('', HomeEventosView.as_view(), name='homeEvents'), 
]