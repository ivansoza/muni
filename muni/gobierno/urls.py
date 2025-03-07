from django.urls import path
from .views import HomeGobiernoView, ListarGabineteView, SemblanzaHomeView, gabinete_list_api, gabinete_update_order_api

urlpatterns = [
    path('', HomeGobiernoView.as_view(), name='homeGobierno'), 
    path('semblanza/', SemblanzaHomeView.as_view(), name='SemblanzaHomeView'), 


    #ADMIN
    path('lista-gabinete/', ListarGabineteView.as_view(), name='ListarGabineteView'), 
    path('gabinete/list/', gabinete_list_api, name='gabinete_list_api'),
    path('gabinete/update-order/', gabinete_update_order_api, name='gabinete_update_order_api'),



]