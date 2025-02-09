# app_name/context_processors.py

def user_info(request):
    user = request.user
    context = {
        # Información del usuario
        'user_first_name': user.first_name if user.is_authenticated and user.first_name else "nombre anonimo",
        'user_username': user.username if user.is_authenticated else "usuario anonimo",
    }

    return context