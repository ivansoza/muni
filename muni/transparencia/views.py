from django.shortcuts import render
from django.views.generic.base import TemplateView
# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt
from .models import SeccionTransparencia
from django.shortcuts import get_object_or_404
from .models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia
from collections import defaultdict
import json  # Para visualizar los datos en la consola

from informacion_municipal.models import Municipio
from .models import Encuesta, Envio, Opcion, Pregunta, Respuesta
# Create your views here.
class HomeTransparenciaView(TemplateView):
    template_name = 'homeTransparencia.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sidebar'] = 'transparecnia'

        return context


class HomeReportesView(TemplateView):
    template_name = 'reportes/reportes.html' 



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

    template_name = 'homeTransparencia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['secciones'] = SeccionTransparencia.objects.all()  # Obtener todas las secciones
        return context
    
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


