from django.urls import path
from .views import DirectorCreateView, DirectorUpdateView, HomeGobiernoView, ListarGabineteView, MiembroGabineteCreateView, MiembroGabineteUpdateView, RegidorCreateView, RegidorUpdateView, SemblanzaHomeView, directores_list_api, directores_update_order_api, gabinete_list_api, gabinete_update_order_api, regidores_list_api, regidores_update_order_api

urlpatterns = [
    path('', HomeGobiernoView.as_view(), name='homeGobierno'), 
    path('semblanza/', SemblanzaHomeView.as_view(), name='SemblanzaHomeView'), 


    #ADMIN
    path('lista-gabinete/', ListarGabineteView.as_view(), name='ListarGabineteView'), 

    # API – lista
    path('api/gabinete/', gabinete_list_api, name='gabinete_list_api'),
    path('api/regidores/', regidores_list_api, name='regidores_list_api'),
    path('api/directores/', directores_list_api, name='directores_list_api'),



    path('api/gabinete/order/', gabinete_update_order_api, name='gabinete_update_order_api'),
    path('api/regidores/order/', regidores_update_order_api, name='regidores_update_order_api'),
    path('api/directores/order/', directores_update_order_api, name='directores_update_order_api'),



    path('gabinete/update-order/', gabinete_update_order_api, name='gabinete_update_order_api'),
    path('crear/', MiembroGabineteCreateView.as_view(), name='gabinete_create'),
    path('editar/<int:pk>/', MiembroGabineteUpdateView.as_view(), name='gabinete_edit'),



    # CRUD páginas (ya tienes la de gabinete; agrega estas)
    path('regidores/add/', RegidorCreateView.as_view(), name='regidor_create'),
    path('regidores/<int:pk>/edit/', RegidorUpdateView.as_view(), name='regidor_edit'),
    path('directores/add/', DirectorCreateView.as_view(), name='director_create'),
    path('directores/<int:pk>/edit/', DirectorUpdateView.as_view(), name='director_edit'),

]