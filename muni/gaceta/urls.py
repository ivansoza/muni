from django.urls import path
from .views import HomeGacetaView

urlpatterns = [
    path('', HomeGacetaView.as_view(), name='homeGaceta'),
]