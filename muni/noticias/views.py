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
        context['sidebar'] = 'noticias' 

        noticias = Noticia.objects.all().order_by('-fecha')

        fecha = self.request.GET.get('fecha', None)
        categoria_id = self.request.GET.get('categoria', None)
        busqueda = self.request.GET.get('buscar', None)

        if fecha:
            noticias = noticias.filter(fecha__date=fecha)
        if categoria_id:
            noticias = noticias.filter(categoria__id=categoria_id)
        if busqueda:
            noticias = noticias.filter(Q(titulo__icontains=busqueda) | Q(contenido__icontains=busqueda))

        paginator = Paginator(noticias, 8)
        page_number = self.request.GET.get('page')
        noticias_page = paginator.get_page(page_number)

        noticias_destacadas = noticias[:4]
        categorias = Categoria.objects.filter(noticias__isnull=False).distinct()
        noticias_por_categoria = {
            categoria.nombre: categoria.noticias.all().order_by('-fecha') 
            for categoria in categorias
        }
        noticias_sidebar = noticias

        # --- NUEVO: calcular rango visible de páginas ---
        total_pages = paginator.num_pages
        current_page = noticias_page.number
        max_pages = 6  # máximo páginas a mostrar en paginación

        half = max_pages // 2
        if total_pages <= max_pages:
            start_page = 1
            end_page = total_pages
        else:
            if current_page <= half:
                start_page = 1
                end_page = max_pages
            elif current_page + half >= total_pages:
                start_page = total_pages - max_pages + 1
                end_page = total_pages
            else:
                start_page = current_page - half
                end_page = current_page + half

        page_range = range(start_page, end_page + 1)

        context['noticias'] = noticias_page
        context['categorias'] = categorias
        context['noticias_por_categoria'] = noticias_por_categoria
        context['noticias_destacadas'] = noticias_destacadas
        context['noticias_sidebar'] = noticias_sidebar
        context['page_range'] = page_range  # Páginas a mostrar en template
        return context


class DetalleNoticiaView(DetailView):
    model = Noticia
    template_name = 'detalleNoticia.html'
    context_object_name = 'noticia'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'noticias'  # Define qué opción está activa
        return context
