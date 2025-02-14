from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Noticia, Categoria

# Create your views here.

class HomeNoticiasView(TemplateView):
    template_name = 'homeNoticias.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'noticias'  # Define qué opción está activa
        
        # Obtener todas las noticias ordenadas por fecha
        noticias = Noticia.objects.all().order_by('-fecha')

        # Filtrado por fecha y categoría (si existen parámetros)
        fecha = self.request.GET.get('fecha', None)
        categoria_id = self.request.GET.get('categoria', None)
        
        if fecha:
            noticias = noticias.filter(fecha__date=fecha)  # Filtrar por fecha específica
        if categoria_id:
            noticias = noticias.filter(categoria__id=categoria_id)  # Filtrar por ID de categoría

        # Obtener solo las categorías que tienen al menos una noticia
        categorias = Categoria.objects.filter(noticias__isnull=False).distinct()

        # Noticias agrupadas por categoría (Solo categorías con noticias)
        noticias_por_categoria = {
            categoria.nombre: categoria.noticias.all().order_by('-fecha') 
            for categoria in categorias
        }

        context['noticias'] = noticias
        context['noticias_por_categoria'] = noticias_por_categoria
        context['categorias'] = categorias  # Pasamos solo las categorías con noticias
        return context
    

class DetalleNoticiaView(DetailView):
    model = Noticia
    template_name = 'detalleNoticia.html'
    context_object_name = 'noticia'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'noticias'  # Define qué opción está activa
        return context
