from django.urls import path
from .views import HomeEventosView, HomeHablaView, articulo_detalle, dar_like

urlpatterns = [
    path('', HomeEventosView.as_view(), name='homeEvents'), 
    path('habla-con-tu-hijo', HomeHablaView.as_view(), name='homeHabla'), 
    path('habla-con-tu-hijo/articulo/<int:id>/', articulo_detalle, name='articuloHabla'), 
    path('dar-like/<int:articulo_id>/', dar_like, name='dar_like'),

]