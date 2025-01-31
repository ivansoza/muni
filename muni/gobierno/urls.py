from django.urls import path
from .views import HomeGobiernoView

urlpatterns = [
    path('', HomeGobiernoView.as_view(), name='homeGobierno'), 
]