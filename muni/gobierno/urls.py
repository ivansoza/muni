from django.urls import path
from .views import CoordinadorDifCreateView, CoordinadorDifUpdateView, DirectorCreateView, DirectorUpdateView, HomeGobiernoView, ListarGabineteView, MiembroGabineteCreateView, MiembroGabineteUpdateView, PresidenteComuCreateView, PresidenteComuUpdateView, RegidorCreateView, RegidorUpdateView, SemblanzaHomeView, coordinadores_dif_list_api, coordinadores_dif_update_order_api, directores_list_api, directores_update_order_api, gabinete_list_api, gabinete_update_order_api, presidentes_comu_list_api, presidentes_comu_update_order_api, regidores_list_api, regidores_update_order_api

urlpatterns = [
    path('', HomeGobiernoView.as_view(), name='homeGobierno'), 
    path('semblanza/', SemblanzaHomeView.as_view(), name='SemblanzaHomeView'), 


    #ADMIN
    path('lista-gabinete/', ListarGabineteView.as_view(), name='ListarGabineteView'), 

    # API – lista
    path('api/gabinete/', gabinete_list_api, name='gabinete_list_api'),
    path('api/regidores/', regidores_list_api, name='regidores_list_api'),
    path('api/directores/', directores_list_api, name='directores_list_api'),
    path('api/presidentes-comu/', presidentes_comu_list_api, name='api-presidentes-comu'),
    path('api/coordinadores-dif/', coordinadores_dif_list_api, name='api-coordinadores-dif'),


    path('api/gabinete/order/', gabinete_update_order_api, name='gabinete_update_order_api'),
    path('api/regidores/order/', regidores_update_order_api, name='regidores_update_order_api'),
    path('api/directores/order/', directores_update_order_api, name='directores_update_order_api'),
    path('api/presidentes-comu/order/',presidentes_comu_update_order_api,name='api-update-order-presidentes-comu'),
    path('api/coordinadores-dif/order/',coordinadores_dif_update_order_api,name='api-update-order-coordinadores-dif'),

    path('gabinete/update-order/', gabinete_update_order_api, name='gabinete_update_order_api'),
    path('crear/', MiembroGabineteCreateView.as_view(), name='gabinete_create'),
    path('editar/<int:pk>/', MiembroGabineteUpdateView.as_view(), name='gabinete_edit'),



    # CRUD páginas (ya tienes la de gabinete; agrega estas)
    path('regidores/add/', RegidorCreateView.as_view(), name='regidor_create'),
    path('regidores/<int:pk>/edit/', RegidorUpdateView.as_view(), name='regidor_edit'),
    path('directores/add/', DirectorCreateView.as_view(), name='director_create'),
    path('directores/<int:pk>/edit/', DirectorUpdateView.as_view(), name='director_edit'),



    # Presidentes Comunales
    path('presidentes-comu/create/', PresidenteComuCreateView.as_view(), name='crear-presidente-comu'),
    path('presidentes-comu/<int:pk>/edit/', PresidenteComuUpdateView.as_view(), name='editar-presidente-comu'),

    # Coordinadores DIF
    path('coordinadores-dif/create/', CoordinadorDifCreateView.as_view(), name='crear-coordinador-dif'),
    path('coordinadores-dif/<int:pk>/edit/', CoordinadorDifUpdateView.as_view(), name='editar-coordinador-dif'),

]