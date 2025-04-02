from django.urls import path
from .views import PerfilUsuarioView

urlpatterns = [
    path('mi-perfil/', PerfilUsuarioView.as_view(), name='perfil_usuario'),

]
