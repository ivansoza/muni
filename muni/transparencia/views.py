from django.shortcuts import render
from django.views.generic.base import TemplateView
# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt

from informacion_municipal.models import Municipio
from .models import Encuesta, Envio, Opcion, Pregunta, Respuesta
# Create your views here.
class HomeTransparenciaView(TemplateView):
    template_name = 'homeTransparencia.html' 




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
