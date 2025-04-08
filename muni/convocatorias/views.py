from django.shortcuts import render
from django.views.generic.base import TemplateView

from generales.models import SeccionPlus
from .models import Convocatoria, Categoria
from datetime import date, timedelta
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, reverse
from datetime import datetime

# Create your views here.
class HomeConvocatoriasView(TemplateView):
    template_name = 'homeConvocatorias.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'mas'  
        
        # Filtrar convocatorias
        context['convocatorias_activas'] = Convocatoria.objects.filter(estado__in=['ABIERTA', 'PRÓXIMA']).order_by('-id')
        context['convocatorias_pasadas'] = Convocatoria.objects.filter(estado='CERRADA').order_by('-id')
        context['categorias'] = Categoria.objects.all()  # Agrega las categorías al contexto

        return context

def filtrar_convocatorias(request):
    categoria = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')
    fecha_filtro = request.GET.get('fecha', '')
    pestana = request.GET.get('pestana', 'active')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 6))
    query = request.GET.get('query', '').lower()
    convocatorias = Convocatoria.objects.all()

    if query:
     convocatorias = convocatorias.filter(titulo__icontains=query)

    if categoria:
        convocatorias = convocatorias.filter(categoria__nombre__icontains=categoria)

    if estado:
        estados_dict = {
            'active': 'ABIERTA',
            'upcoming': 'PRÓXIMA',
            'closed': 'CERRADA'
        }
        if estado in estados_dict:
            convocatorias = convocatorias.filter(estado=estados_dict[estado])

    if fecha_filtro == "this-week":
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=7)
        convocatorias = convocatorias.filter(fecha_apertura__range=(start_date, end_date))
    elif fecha_filtro == "this-month":
        start_date = timezone.now().replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        convocatorias = convocatorias.filter(fecha_apertura__range=(start_date, end_date))
    elif fecha_filtro == "next-month":
        start_date = (timezone.now().replace(day=1) + timedelta(days=32)).replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        convocatorias = convocatorias.filter(fecha_apertura__range=(start_date, end_date))

    if pestana == "active":
        convocatorias = convocatorias.filter(estado__in=['ABIERTA', 'PRÓXIMA'])
    elif pestana == "past":
        convocatorias = convocatorias.filter(estado='CERRADA')

    paginator = Paginator(convocatorias, per_page)
    page_obj = paginator.get_page(page)

    data = {
        "convocatorias": [
            {
                "id": conv.id,
                "titulo": conv.titulo,
                "estado": conv.estado,
                "categoria": conv.categoria.nombre,
                "descripcion": conv.descripcion,
                "imagen": conv.imagen.url,
                "fecha_apertura": conv.fecha_apertura.strftime("%d/%m/%Y"),
                "fecha_cierre": conv.fecha_cierre.strftime("%d/%m/%Y"),
            }
            for conv in page_obj
        ],
        "total_pages": paginator.num_pages,
        "current_page": page_obj.number,
    }
    return JsonResponse(data)



def filtrar_convocatorias_seccion_plus(request, seccion_pk):
    """
    Devuelve (en JSON) las convocatorias que pertenecen a la misma categoría que la SeccionPlus
    indicada y que cumplen los filtros recibidos por GET.
    """
    # ------------------------------------------------------------------ Sección
    seccion = get_object_or_404(SeccionPlus, pk=seccion_pk, status=True)
    convocatorias = Convocatoria.objects.filter(
        categoria=seccion.categoria_convocatoria
    )

    # ------------------------------------------------------------------ Filtros
    query        = request.GET.get("query", "").strip().lower()
    categoria    = request.GET.get("categoria", "").strip()
    estado       = request.GET.get("estado", "").strip()
    fecha_filtro = request.GET.get("fecha", "").strip()
    pestana      = request.GET.get("pestana", "active").strip()

    # Page y per_page robustos
    page_param     = request.GET.get("page", "1")
    per_page_param = request.GET.get("per_page", "6")
    try:
        page = int(page_param)
    except ValueError:
        page = 1
    try:
        per_page = int(per_page_param)
    except ValueError:
        per_page = 6

    if query:
        convocatorias = convocatorias.filter(titulo__icontains=query)

    if categoria:
        convocatorias = convocatorias.filter(categoria__nombre__icontains=categoria)

    if estado:
        estados_dict = {"active": "ABIERTA", "upcoming": "PRÓXIMA", "closed": "CERRADA"}
        if estado in estados_dict:
            convocatorias = convocatorias.filter(estado=estados_dict[estado])

    from datetime import timedelta
    today = timezone.now().date()
    if fecha_filtro == "this-week":
        end_date = today + timedelta(days=7)
        convocatorias = convocatorias.filter(fecha_apertura__range=(today, end_date))
    elif fecha_filtro == "this-month":
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        convocatorias = convocatorias.filter(fecha_apertura__range=(start_date, end_date))
    elif fecha_filtro == "next-month":
        start_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        convocatorias = convocatorias.filter(fecha_apertura__range=(start_date, end_date))

    if pestana == "active":
        convocatorias = convocatorias.filter(estado__in=["ABIERTA", "PRÓXIMA"])
    elif pestana == "past":
        convocatorias = convocatorias.filter(estado="CERRADA")

    # ------------------------------------------------------------------ Paginación
    convocatorias = convocatorias.order_by("-id")
    paginator     = Paginator(convocatorias, per_page)
    page_obj      = paginator.get_page(page)

    # ------------------------------------------------------------------ Serialización de respuesta
    data = {
        "convocatorias": [
            {
                "id": conv.id,
                "titulo": conv.titulo,
                "estado": conv.estado,
                "categoria": conv.categoria.nombre,
                "descripcion": conv.descripcion,
                # Se comprueba si hay imagen, en caso contrario se asigna cadena vacía
                "imagen": conv.imagen.url if conv.imagen else "",
                "fecha_apertura": conv.fecha_apertura.strftime("%d/%m/%Y"),
                "fecha_cierre": conv.fecha_cierre.strftime("%d/%m/%Y"),
            }
            for conv in page_obj
        ],
        "total_pages": paginator.num_pages,
        "current_page": page_obj.number,
    }
    return JsonResponse(data)

class detalleConvocatoria(TemplateView):
    template_name = 'detalleConvocatoria.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        convocatoria_id = self.kwargs.get('id')
        convocatoria = get_object_or_404(Convocatoria, id=convocatoria_id)

        # Cálculos de fechas y avance
        fecha_apertura = convocatoria.fecha_apertura
        fecha_cierre = convocatoria.fecha_cierre
        fecha_actual = datetime.now().date()

        dias_totales = (fecha_cierre - fecha_apertura).days
        dias_restantes = (fecha_cierre - fecha_actual).days
        dias_transcurridos = dias_totales - dias_restantes

        porcentaje_avance = 0
        if dias_totales > 0:
            porcentaje_avance = (dias_transcurridos / dias_totales) * 100

        # Evitar valores negativos o mayores a 100
        porcentaje_avance = max(0, min(porcentaje_avance, 100))

        # Asignación de variables en el contexto
        context['convocatoria'] = convocatoria
        context['tiempo_restante'] = dias_restantes if dias_restantes > 0 else 0
        context['porcentaje_avance'] = porcentaje_avance
        context['dias_totales'] = dias_totales

        # Si se recibe seccion_id (desde la URL anidada) se configura la URL de regreso
        seccion_id = self.kwargs.get('seccion_id')
        if seccion_id:
            seccion = get_object_or_404(SeccionPlus, id=seccion_id)
            context['seccion_origen'] = seccion
            # Aquí se construye la URL para volver a la sección correspondiente,
            # asumiendo que tienes una ruta con nombre 'seccionplus_detail'
            context['url_volver'] = reverse('seccionplus_detail', kwargs={'pk': seccion.pk, 'slug': seccion.slug})
        else:
            # Si no viene seccion_id, se regresa al listado general de convocatorias
            context['url_volver'] = reverse('HomeConvocatoriasView')

        return context