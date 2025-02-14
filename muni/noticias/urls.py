from django.urls import path
from .views import HomeNoticiasView, DetalleNoticiaView

urlpatterns = [
    path('', HomeNoticiasView.as_view(), name='homeNoticias'), 
    path('noticia/<int:pk>/', DetalleNoticiaView.as_view(), name='detalle_noticia'),
]