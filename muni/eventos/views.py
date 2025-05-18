from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Articulo, Categoria
from django.shortcuts import render, get_object_or_404
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

# Create your views here.
class HomeEventosView(TemplateView):
    template_name = 'homeEvents.html' 


class HomeHablaView(TemplateView):
    template_name = 'homeHabla.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el artículo destacado (el último con `destacado=True`)
        context['articulo_destacado'] = Articulo.objects.filter(destacado=True).order_by('-fecha_publicacion').first()

        # Obtener los artículos más recientes (excluyendo el destacado si existe)
        context['articulos_recientes'] = Articulo.objects.exclude(id=context['articulo_destacado'].id if context['articulo_destacado'] else None).order_by('-fecha_publicacion')

        # Obtener todas las categorías disponibles
        categorias = Categoria.objects.all()
        context['categorias'] = categorias

        return context

def articulo_detalle(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    comentarios = articulo.comentarios.all()
    etiquetas = articulo.etiquetas.split(',')
    articulo_anterior = Articulo.objects.filter(id__lt=articulo.id).order_by('-id').first()
    articulo_siguiente = Articulo.objects.filter(id__gt=articulo.id).order_by('id').first()

    # Artículos relacionados (4 aleatorios)
    articulos_relacionados = list(Articulo.objects.exclude(id=articulo.id))
    if len(articulos_relacionados) > 4:
        articulos_relacionados = random.sample(articulos_relacionados, 4)

    # Convertir el link de video a embed si existe
    video_embed_url = convertir_a_embed(articulo.video_url)

    return render(request, 'articulo_habla.html', {
        'articulo': articulo,
        'comentarios': comentarios,
        'etiquetas': etiquetas,
        'articulo_anterior': articulo_anterior,
        'articulo_siguiente': articulo_siguiente,
        'articulos_relacionados': articulos_relacionados,
        'video_embed_url': video_embed_url,
    })

def convertir_a_embed(url):
    if not url:
        return None
    if "youtube.com/watch?v=" in url:
        return url.replace("watch?v=", "embed/")
    elif "youtu.be/" in url:
        video_id = url.split("/")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    elif "vimeo.com/" in url:
        video_id = url.split("/")[-1]
        return f"https://player.vimeo.com/video/{video_id}"
    return url  # En caso de que sea otra plataforma

@csrf_exempt
def dar_like(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    user_ip = get_client_ip(request)  # Obtener la IP del usuario

    # Guardar las IPs que dieron like en caché o base de datos
    ip_key = f"liked_{articulo_id}_{user_ip}"
    already_liked = cache.get(ip_key)

    if already_liked:
        return JsonResponse({'likes': articulo.likes, 'liked': False})  # Ya había dado like

    # Dar like y registrar la IP
    articulo.likes += 1
    articulo.save()
    cache.set(ip_key, True, timeout=60*60*24)  # Se guarda por 24h

    return JsonResponse({'likes': articulo.likes, 'liked': True})

def get_client_ip(request):
    """Obtiene la dirección IP del usuario"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
