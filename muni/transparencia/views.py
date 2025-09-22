from django.shortcuts import render
from django.views.generic.base import TemplateView
# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.apps import apps
from django.utils import timezone
from django.core.mail import send_mail

from transparencia.forms import ReporteAlcantarilladoForm, ReporteAlumbradoPublicoForm, ReporteBacheForm, ReporteServicioAguaForm
from reportes.models import ReporteStatus
from .models import ArticuloLiga, SeccionTransparencia
from django.shortcuts import get_object_or_404
from .models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia
from collections import defaultdict
import json  # Para visualizar los datos en la consola
from django.db.models import Prefetch

from informacion_municipal.models import Municipio
from .models import Encuesta, Envio, Opcion, Pregunta, Respuesta
from django.shortcuts import render
from .models import ListaObligaciones, LigaArchivo
# Create your views here.
class HomeTransparenciaView(TemplateView):
    template_name = 'homeTransparencia.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sidebar'] = 'transparecnia'
        context['secciones'] = SeccionTransparencia.objects.all()  # Obtener todas las secciones

        return context
    


class HomeSevacView(TemplateView):
    template_name = 'homeSevac.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'sevac'


        return context
    




class HomeReportesView(TemplateView):
    template_name = 'reportes/reportes.html' 


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ─── get_or_create del único ReporteStatus ───
        defaults = {
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        }

        reporte_status, _ = ReporteStatus.objects.get_or_create(
            pk=1,  # siempre usaremos el registro #1
            defaults=defaults,
        )

        context["reporte_status"] = reporte_status
        context['sidebar'] = 'reportes'
        return context



class HomeReportesView(TemplateView):
    template_name = 'reportes/reportes.html' 


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ─── get_or_create del único ReporteStatus ───
        defaults = {
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        }

        reporte_status, _ = ReporteStatus.objects.get_or_create(
            pk=1,  # siempre usaremos el registro #1
            defaults=defaults,
        )

        context["reporte_status"] = reporte_status
        context['sidebar'] = 'reportes'
        return context
def get_encuestas_activas(request, municipio_id):
    """
    Devuelve todas las encuestas activas de un municipio, con sus preguntas y opciones.
    """
    municipio = get_object_or_404(Municipio, pk=municipio_id, status='activo')
    encuestas = Encuesta.objects.filter(municipio=municipio, estado='activo')

    if not encuestas.exists():
        return JsonResponse({"detail": "No hay encuestas activas disponibles."}, status=404)

    data = []
    for encuesta in encuestas:
        encuesta_dict = {
            "id": encuesta.id,
            "titulo": encuesta.titulo,
            "descripcion": encuesta.descripcion,
            "preguntas": []
        }
        for pregunta in encuesta.preguntas.all().order_by('orden'):
            pregunta_dict = {
                "id": pregunta.id,
                "texto": pregunta.texto,
                "opciones": []
            }
            for opcion in pregunta.opciones.all():
                pregunta_dict["opciones"].append({
                    "id": opcion.id,
                    "texto": opcion.texto
                })
            encuesta_dict["preguntas"].append(pregunta_dict)
        data.append(encuesta_dict)

    # Devolvemos un array de encuestas (safe=False)
    return JsonResponse(data, safe=False, status=200)


@csrf_exempt
def guardar_respuestas(request):
    """
    Guarda las respuestas de un usuario a la encuesta en Envio y Respuesta.
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        encuesta_id = body.get('encuesta_id')
        respuestas_data = body.get('respuestas', [])

        if not encuesta_id or not respuestas_data:
            return JsonResponse({"detail": "Datos incompletos."}, status=400)

        # Verificamos que la encuesta exista y esté activa
        try:
            encuesta = Encuesta.objects.get(id=encuesta_id, estado='activo')
        except Encuesta.DoesNotExist:
            return JsonResponse({"detail": "Encuesta no encontrada o inactiva."}, status=404)

        # Creamos un Envio
        envio = Envio.objects.create(encuesta=encuesta)

        # Creamos cada Respuesta
        for r in respuestas_data:
            pregunta_id = r.get('pregunta_id')
            opcion_id = r.get('opcion_id')

            try:
                pregunta = Pregunta.objects.get(id=pregunta_id, encuesta=encuesta)
                opcion = Opcion.objects.get(id=opcion_id, pregunta=pregunta)
            except (Pregunta.DoesNotExist, Opcion.DoesNotExist):
                continue  # O manejar error

            Respuesta.objects.create(
                envio=envio, 
                pregunta=pregunta, 
                opcion=opcion
            )

        return JsonResponse({"detail": "Respuestas guardadas correctamente."}, status=201)

    return JsonResponse({"detail": "Método no permitido."}, status=405)


    
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia

class EjerciciosPorSeccionView(TemplateView):
    template_name = 'ejercicios_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seccion_id = self.kwargs.get('seccion_id')
        seccion = get_object_or_404(SeccionTransparencia, id=seccion_id)
        ejercicios = EjercicioFiscal.objects.filter(seccion=seccion).prefetch_related('documentos')

        documentos_organizados = []

        for ejercicio in ejercicios:
            datos_ejercicio = {
                "ejercicio_id": ejercicio.id,
                "ejercicio_nombre": ejercicio.nombre,
                "años": {},
                "directos": []  # 📌 Aquí guardaremos los documentos SIN AÑO NI MES dentro del ejercicio
            }

            for doc in ejercicio.documentos.all():
                año = str(doc.año) if doc.año else None
                mes = dict(DocumentoTransparencia.MESES).get(doc.mes, "Sin Mes") if doc.mes else None

                if año:
                    if año not in datos_ejercicio["años"]:
                        datos_ejercicio["años"][año] = {"meses": {}, "directos": []}

                    if doc.mes:
                        datos_ejercicio["años"][año]["meses"].setdefault(mes, []).append(doc)
                    else:
                        datos_ejercicio["años"][año]["directos"].append(doc)
                else:
                    datos_ejercicio["directos"].append(doc)  # 📌 Ahora se guarda en "directos" dentro del ejercicio

            documentos_organizados.append(datos_ejercicio)

        context['seccion'] = seccion
        context['documentos_organizados'] = documentos_organizados
        return context




def lista_obligaciones(request):
    # Definimos el prefetch para ligaarchivo en el contexto de ArticuloLiga
    liga_prefetch = Prefetch(
        'ligaarchivo_set',
        queryset=LigaArchivo.objects.order_by('-ano'),
        to_attr='archivos'
    )

    # Ahora prefetch_related sobre los artículos (articulos_liga)
    lista_obligaciones = (
        ListaObligaciones.objects
        .all()
        .prefetch_related(
            Prefetch('articulos_liga', queryset=ArticuloLiga.objects.prefetch_related(liga_prefetch))
        )
    )

    # Obtenemos los años disponibles desde el modelo LigaArchivo
    years = (
        LigaArchivo.objects
        .exclude(ano__isnull=True)
        .values_list('ano', flat=True)
        .distinct()
        .order_by('-ano')
    )

    return render(request, 'listaTrasnparencia.html', {
        'lista_obligaciones': lista_obligaciones,
        'years': years,
        'sidebar': 'transparencia'
    })





# ───────────────────  Mixin para evitar repetición ────────────────────
class ReporteStatusMixin:
    sidebar_value = "reportes"

    def get_tipo_url(self, reporte):
        # Relaciona el modelo con el tipo usado en la URL
        from reportes.models import (
            ReporteServicioAgua,
            ReporteBache,
            ReporteAlcantarillado,
            ReporteAlumbradoPublico,
        )
        if isinstance(reporte, ReporteServicioAgua):
            return "agua"
        elif isinstance(reporte, ReporteBache):
            return "bache"
        elif isinstance(reporte, ReporteAlcantarillado):
            return "alcantarillado"
        elif isinstance(reporte, ReporteAlumbradoPublico):
            return "alumbrado"
        return "desconocido"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        defaults = {
            "reporte_agua_status": False,
            "reporte_bache_status": False,
            "reporte_alcantarillado_status": False,
            "reporte_alumbrado_status": False,
        }
        status, _ = ReporteStatus.objects.get_or_create(pk=1, defaults=defaults)

        ctx["reporte_status"] = status
        ctx["sidebar"] = self.sidebar_value
        return ctx

    # helper genérico para el POST
    def _process_form(self, form_cls, request):
        form = form_cls(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save()
            tipo_reporte = reporte._meta.verbose_name.title()
            status = ReporteStatus.objects.get(pk=1)
            # Selecciona el correo según el tipo de reporte
            if tipo_reporte.lower() == "reporte de servicio de agua":
                destinatario = status.correo_agua
            elif tipo_reporte.lower() == "reporte de bache":
                destinatario = status.correo_bache
            elif tipo_reporte.lower() == "reporte de alcantarillado":
                destinatario = status.correo_alcantarillado
            elif tipo_reporte.lower() == "reporte de alumbrado público":
                destinatario = status.correo_alumbrado
            else:
                destinatario = None

            asunto = f"{reporte.codigo_seguimiento} - {tipo_reporte}"
            tipo_url = self.get_tipo_url(reporte)
            gestion_url = f"http://127.0.0.1:8000/reportes/admin/generales/reportes/{tipo_url}/{reporte.pk}/"
            mensaje = (
                f"<h2 style='color:#2c3e50;'>Nuevo {tipo_reporte} recibido</h2>"
                f"<p><strong>Nombre:</strong> {reporte.nombre_solicitante}</p>"
                f"<p><strong>Descripción:</strong> {reporte.descripcion}</p>"
                f"<p><strong>Ubicación:</strong> {reporte.ubicacion}</p>"
                f"<p><strong>Código de seguimiento:</strong> <span style='color:#2980b9;'>{reporte.codigo_seguimiento}</span></p>"
                f"<p><strong>Gestionar reporte:</strong> <a href='{gestion_url}' style='color:#27ae60;'>Abrir en panel de administración</a></p>"
            )

            if destinatario:
                send_mail(
                    asunto,
                    mensaje,
                    "no-responder@siptlax.com",
                    [destinatario],
                    fail_silently=True,
                    html_message=mensaje
                )

            return JsonResponse(
                {"success": True, "codigo_seguimiento": reporte.codigo_seguimiento}
            )
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


# ───────────────────  Vistas ────────────────────
class ReporteServicioAguaView(ReporteStatusMixin, TemplateView):
    template_name = "reportes/servicio_agua.html"

    def post(self, request, *args, **kwargs):
        return self._process_form(ReporteServicioAguaForm, request)


class ReporteBacheView(ReporteStatusMixin, TemplateView):
    template_name = "reportes/bache.html"

    def post(self, request, *args, **kwargs):
        return self._process_form(ReporteBacheForm, request)


class ReporteAlcantarilladoView(ReporteStatusMixin, TemplateView):
    template_name = "reportes/alcantarillado.html"

    def post(self, request, *args, **kwargs):
        return self._process_form(ReporteAlcantarilladoForm, request)


class ReporteAlumbradoPublicoView(ReporteStatusMixin, TemplateView):
    template_name = "reportes/alumbrado_publico.html"

    def post(self, request, *args, **kwargs):
        return self._process_form(ReporteAlumbradoPublicoForm, request)



@require_GET
def consulta_reporte_ajax(request):
    codigo = request.GET.get("codigo", "").strip()
    if not codigo:
        return JsonResponse({"error": "No se proporcionó código"}, status=400)

    modelos = [
        apps.get_model("reportes", "ReporteServicioAgua"),
        apps.get_model("reportes", "ReporteBache"),
        apps.get_model("reportes", "ReporteAlcantarillado"),
        apps.get_model("reportes", "ReporteAlumbradoPublico"),
    ]

    reporte = None
    tipo = ""
    for m in modelos:
        try:
            reporte = m.objects.get(codigo_seguimiento=codigo)
            tipo = m._meta.verbose_name.title()
            break
        except m.DoesNotExist:
            continue

    if reporte is None:
        return JsonResponse({"error": "Código no encontrado"}, status=404)

    # Usamos localtime para cada fecha
    def fmt(dt):
        return timezone.localtime(dt).strftime("%Y-%m-%d %H:%M") if dt else ""

    data = {
        "tipo": tipo,
        "codigo": reporte.codigo_seguimiento,
        "nombre": reporte.nombre_solicitante,
        "descripcion": reporte.descripcion,
        "estatus": reporte.get_estatus_display(),
        "comentarios_internos": reporte.comentarios or "",
        "ubicacion": reporte.ubicacion,
        "latitud": str(reporte.latitud) if reporte.latitud is not None else "",
        "longitud": str(reporte.longitud) if reporte.longitud is not None else "",
        "place_id": reporte.place_id or "",
        "fecha_creado": fmt(reporte.creado),
        "fecha_pendiente": fmt(reporte.fecha_pendiente),
        "fecha_en_progreso": fmt(reporte.fecha_en_progreso),
        "fecha_resuelto": fmt(reporte.fecha_resuelto),
        "fecha_cerrado": fmt(reporte.fecha_cerrado),
        "foto_url": reporte.foto.url if reporte.foto else "",
    }

    return JsonResponse({"reporte": data})