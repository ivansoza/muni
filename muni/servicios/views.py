from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from servicios.models import ComoLoRealizo, ConfiguracionServicio, CuantoCuesta, EnQueConsiste, QueSeRequiere, RequisitosImagen, Servicio
from django.template.loader import render_to_string
from django.http import JsonResponse

class HomeServiciosView(TemplateView):
    template_name = ''

    def dispatch(self, request, *args, **kwargs):
        config = ConfiguracionServicio.objects.first()
        self.template_name = 'homeServiciosV2.html' if (config and config.usar_plantilla_v2) else 'homeServicios.html'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'servicios'  # Define qué opción está activa

        servicios = Servicio.objects.all()

        # Filtrar por búsqueda
        query = self.request.GET.get('q', '')
        clasificacion = self.request.GET.get('clasificacion', '')
        sector = self.request.GET.get('sector', '')
        organismo = self.request.GET.get('organismo', '')
        per_page = self.request.GET.get('per_page', '12')

        # Aplicar búsqueda por título
        if query:
            servicios = servicios.filter(titulo__icontains=query)

        # Aplicar filtros según categoría, sector y organismo
        if clasificacion:
            servicios = servicios.filter(clasificacion__id=clasificacion)
        if sector:
            servicios = servicios.filter(sector__id=sector)
        if organismo:
            servicios = servicios.filter(organismo__id=organismo)

        # Configurar paginación
        paginator = Paginator(servicios, int(per_page))
        page = self.request.GET.get('page', 1)
        servicios_paginados = paginator.get_page(page)

        # Pasar datos al template
        context.update({
            'servicios': servicios_paginados,
            'query': query,
            'clasificacion': clasificacion,
            'sector': sector,
            'organismo': organismo,
            'per_page': per_page,
            'organismos': Servicio.objects.values('organismo__id', 'organismo__nombre').distinct(),
        })
        
        return context

class ServicioDetailView(DetailView):
    model = Servicio
    template_name = "detalle_servicio.html"
    context_object_name = "servicio"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'servicios'

        try:
            context["consiste"] = EnQueConsiste.objects.get(servicio=self.object)
            context["requiere"] = QueSeRequiere.objects.filter(servicio=self.object)
            
            # Los nombres correctos son los almacenados en el campo (clave del choice)
            context["instrucciones_linea"] = ComoLoRealizo.objects.filter(
                servicio=self.object,
                canal_presentacion__nombre='linea'
            ).order_by('paso')

            context["instrucciones_presencial"] = ComoLoRealizo.objects.filter(
                servicio=self.object,
                canal_presentacion__nombre='presencial'
            ).order_by('paso')

            context["costos"] = CuantoCuesta.objects.filter(servicio=self.object)

        except ObjectDoesNotExist:
            context["consiste"] = None
            context['requiere'] = None
            context["instrucciones_linea"] = []
            context["instrucciones_presencial"] = []
            context['costos'] = None
        return context
    
class ServicioDetalleParcialView(DetailView):
    model = Servicio

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        
        try:
            context["consiste"] = EnQueConsiste.objects.get(servicio=self.object)
            context["requiere"] = QueSeRequiere.objects.filter(servicio=self.object)
            context["instrucciones_linea"] = ComoLoRealizo.objects.filter(
                servicio=self.object,
                canal_presentacion__nombre='linea'
            ).order_by('paso')
            context["instrucciones_presencial"] = ComoLoRealizo.objects.filter(
                servicio=self.object,
                canal_presentacion__nombre='presencial'
            ).order_by('paso')
            context["costos"] = CuantoCuesta.objects.filter(servicio=self.object)
        except ObjectDoesNotExist:
            context["consiste"] = None
            context['requiere'] = []
            context["instrucciones_linea"] = []
            context["instrucciones_presencial"] = []
            context["costos"] = []

        # Leer la única configuración existente
        config = ConfiguracionServicio.objects.first()

        if config:
            context.update({
                # Secciones
                'mostrar_seccion_consiste': config.mostrar_seccion_consiste,
                'mostrar_seccion_requisitos': config.mostrar_seccion_requisitos,
                'mostrar_seccion_realizo': config.mostrar_seccion_realizo,
                'mostrar_seccion_costo': config.mostrar_seccion_costo,
                'mostrar_seccion_responsable': config.mostrar_seccion_responsable,

                # En qué consiste
                'mostrar_puede_ser_solicitado': config.mostrar_puede_ser_solicitado,

                # Requisitos
                'mostrar_tipo_documento': config.mostrar_tipo_documento,
                'mostrar_presentar_original': config.mostrar_presentar_original,
                'mostrar_presentar_copia': config.mostrar_presentar_copia,
                'mostrar_archivo_descarga': config.mostrar_archivo_descarga,

                # Costos
                'mostrar_observaciones': config.mostrar_observaciones,
                'mostrar_campo_vigencia': config.mostrar_campo_vigencia,
                'mostrar_campo_tipo': config.mostrar_campo_tipo,
                'mostrar_campo_momento_pago': config.mostrar_campo_momento_pago,
            })

        if config:
            context['usar_requisitos_v2'] = config.usar_requisitos_v2
            if config.usar_requisitos_v2:
                context['requisitos_imagen'] = (
                    RequisitosImagen.objects.filter(servicio=self.object).first()
                )

        html = render_to_string('detalle_servicio_p.html', context, request=request)
        return JsonResponse({'html': html})