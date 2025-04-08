from django.urls import path

from generales.views import SeccionPlusDetailView
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  # Homepage
    path('seccion/<int:pk>/<slug:slug>/', SeccionPlusDetailView.as_view(), name='seccionplus_detail'),

]