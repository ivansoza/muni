from django.urls import path
from .views import HomeGobiernoView, ListarGabineteView, SemblanzaHomeView

urlpatterns = [
    path('', HomeGobiernoView.as_view(), name='homeGobierno'), 
    path('semblanza/', SemblanzaHomeView.as_view(), name='SemblanzaHomeView'), 


    #ADMIN
    path('lista-gabinete/', ListarGabineteView.as_view(), name='ListarGabineteView'), 



]