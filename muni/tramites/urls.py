from django.urls import path
from .views import HomeTramitesView

urlpatterns = [
    path('', HomeTramitesView.as_view(), name='homeTramites'), 
]