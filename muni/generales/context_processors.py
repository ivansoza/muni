# app_name/context_processors.py
from informacion_municipal.models import Municipio


def municipio(request):
    municipio_obj = Municipio.objects.filter(status='activo').first()  # Obtiene el primer municipio activo
    return {'municipio': municipio_obj}

def user_info(request):
    user = request.user
    context = {
        # Información del usuario
        'user_first_name': user.first_name if user.is_authenticated and user.first_name else "nombre anonimo",
        'user_username': user.username if user.is_authenticated else "usuario anonimo",
    }

    return context