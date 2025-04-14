# app_name/context_processors.py
from informacion_municipal.models import Municipio
from generales.models import ContadorVisitas


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

    if not user.is_authenticated:
        context['is_superuser'] = False
        context['user_permissions'] = []
    else:
        # Permisos como lista de strings tipo "auth.add_user", "myapp.view_modelo"
        permisos = user.get_all_permissions()
        context['is_superuser'] = user.is_superuser
        context['user_permissions'] = sorted(permisos)  # puedes quitar el sorted() si no necesitas orden


    return context

def contador_visitas_context(request):
    try:
        contador = ContadorVisitas.objects.get(id=1)
        visitas = contador.visitas
    except ContadorVisitas.DoesNotExist:
        visitas = 0
    return {'contador_visitas': visitas}
