from django.urls import path
from .views import HomeEventosView, HomeHablaView

urlpatterns = [
    path('', HomeEventosView.as_view(), name='homeEvents'), 
    path('habla-con-tu-hijo', HomeHablaView.as_view(), name='homeHabla'), 

]