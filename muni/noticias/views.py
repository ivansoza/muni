from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Noticia, Categoria
from django.core.paginator import Paginator
from django.db.models import Q

class HomeNoticiasView(TemplateView):
    template_name = 'homeNoticias.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'noticias'  # Define qué opción está activa

        # Obtener todas las noticias ordenadas por fecha (de la más reciente a la más antigua)
        noticias = Noticia.objects.all().order_by('-fecha')

        # Filtrado por fecha y categoría
        fecha = self.request.GET.get('fecha', None)
        categoria_id = self.request.GET.get('categoria', None)
        busqueda = self.request.GET.get('buscar', None)  # Capturamos el término de búsqueda
        
        if fecha:
            noticias = noticias.filter(fecha__date=fecha)
        if categoria_id:
            noticias = noticias.filter(categoria__id=categoria_id)
        if busqueda:
            noticias = noticias.filter(Q(titulo__icontains=busqueda) | Q(contenido__icontains=busqueda))

        # Paginación: Muestra 8 noticias por página
        paginator = Paginator(noticias, 8)
        page_number = self.request.GET.get('page')
        noticias_page = paginator.get_page(page_number)
        noticias_destacadas = noticias[:3]

        # Obtener las categorías con al menos una noticia
        categorias = Categoria.objects.filter(noticias__isnull=False).distinct()

        # Noticias agrupadas por categoría (Solo categorías con noticias)
        noticias_por_categoria = {
            categoria.nombre: categoria.noticias.all().order_by('-fecha') 
            for categoria in categorias
        }

        # Obtener todas las noticias para el sidebar
        noticias_sidebar = noticias  # Ahora iteramos todas las noticias

        context['noticias'] = noticias_page
        context['categorias'] = categorias
        context['noticias_por_categoria'] = noticias_por_categoria
        context['noticias_destacadas'] = noticias_destacadas
        context['noticias_sidebar'] = noticias_sidebar  # Pasamos todas las noticias al sidebar
        return context



    

class DetalleNoticiaView(DetailView):
    model = Noticia
    template_name = 'detalleNoticia.html'
    context_object_name = 'noticia'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'noticias'  # Define qué opción está activa
        return context
