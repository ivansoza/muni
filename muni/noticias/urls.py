from django.urls import path
from .views import HomeNoticiasView

urlpatterns = [
    path('', HomeNoticiasView.as_view(), name='homeNoticias'), 
]