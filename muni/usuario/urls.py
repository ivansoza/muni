from django.urls import path
from .views import CustomPasswordChangeDoneView, CustomPasswordChangeView, PerfilUsuarioView, UserProfileUpdateView

urlpatterns = [
    path('mi-perfil/', PerfilUsuarioView.as_view(), name='perfil_usuario'),
    path(
        'cambiar-contraseña/',
        CustomPasswordChangeView.as_view(),
        name='password_change'
    ),

    # Confirmación de cambio de contraseña exitoso
    path(
        'cambiar-contraseña/hecho/',
        CustomPasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),

    path('editar-perfil/', UserProfileUpdateView.as_view(), name='editar_perfil'),
]
