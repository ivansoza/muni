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

        # Obtener el parámetro de la URL
        filtro = self.request.GET.get('filtro', None)  # Puede ser 'habla' o 'ven_vive'

        # Filtrar artículos según el filtro
        if filtro == 'habla':
            context['articulos'] = Articulo.objects.filter(habla=True).order_by('-fecha_publicacion')
            # Seleccionar el último artículo de la categoría "Habla con tus hijos"
            context['articulo_destacado'] = Articulo.objects.filter(destacado=True,habla=True).order_by('-fecha_publicacion').first()
        elif filtro == 'ven_vive':
            context['articulos'] = Articulo.objects.filter(ven_vive=True).order_by('-fecha_publicacion')
            # Seleccionar el último artículo de la categoría "Ven vive y vuelve a tu municipio"
            context['articulo_destacado'] = Articulo.objects.filter(destacado=True,ven_vive=True).order_by('-fecha_publicacion').first()
        else:
            context['articulos'] = Articulo.objects.all().order_by('-fecha_publicacion')
            # Si no hay filtro, se selecciona el artículo destacado más reciente
            context['articulo_destacado'] = Articulo.objects.filter(destacado=True).order_by('-fecha_publicacion').first()

        # Incluir el filtro en el contexto
        context['filtro'] = filtro

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

    # Filtrar artículo anterior y siguiente basados en la categoría (habla o ven_vive)
    if articulo.habla:
        articulo_anterior = Articulo.objects.filter(habla=True, id__lt=articulo.id).order_by('-id').first()
        articulo_siguiente = Articulo.objects.filter(habla=True, id__gt=articulo.id).order_by('id').first()
    elif articulo.ven_vive:
        articulo_anterior = Articulo.objects.filter(ven_vive=True, id__lt=articulo.id).order_by('-id').first()
        articulo_siguiente = Articulo.objects.filter(ven_vive=True, id__gt=articulo.id).order_by('id').first()
    else:
        # Si no tiene categoría, mostrar el anterior y siguiente sin filtrar
        articulo_anterior = Articulo.objects.filter(id__lt=articulo.id).order_by('-id').first()
        articulo_siguiente = Articulo.objects.filter(id__gt=articulo.id).order_by('id').first()

    # Artículos relacionados (4 aleatorios) basados en la categoría
    if articulo.habla:
        articulos_relacionados = Articulo.objects.filter(habla=True).exclude(id=articulo.id)
    elif articulo.ven_vive:
        articulos_relacionados = Articulo.objects.filter(ven_vive=True).exclude(id=articulo.id)
    else:
        articulos_relacionados = Articulo.objects.exclude(id=articulo.id)

    # Si hay más de 4 artículos relacionados, seleccionamos 4 aleatorios
    if len(articulos_relacionados) > 4:
        articulos_relacionados = random.sample(list(articulos_relacionados), 4)

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
