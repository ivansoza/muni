from django.urls import path
from .views import HomeGobiernoView, SemblanzaHomeView

urlpatterns = [
    path('', HomeGobiernoView.as_view(), name='homeGobierno'), 
    path('semblanza/', SemblanzaHomeView.as_view(), name='SemblanzaHomeView'), 

]