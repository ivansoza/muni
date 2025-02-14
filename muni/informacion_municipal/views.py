from django.shortcuts import render
from django.views.generic.base import TemplateView
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Municipio, ColoresMunicipio
# Create your views here.
class HomeInformacionView(TemplateView):
    template_name = 'homeInfoMuni.html' 



@csrf_exempt  # Si no deseas manejar CSRF en esta vista (para AJAX directo)
def guardar_colores(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parsear el JSON del body
            municipio_id = data.get('municipio_id')
            color_primario = data.get('color_primario')
            color_secundario = data.get('color_secundario')
            
            if not municipio_id:
                return JsonResponse({'error': 'municipio_id es requerido'}, status=400)
            
            # Buscar el municipio
            municipio = Municipio.objects.get(id=municipio_id)
            
            # Verificar si ya existe un ColoresMunicipio para este municipio
            # (asumiendo que sólo puede existir uno, o tomas el primero)
            colores_obj = municipio.colores.first()
            if not colores_obj:
                # Si no existe, creamos un nuevo objeto
                colores_obj = ColoresMunicipio(municipio=municipio)

            # Asignar los nuevos colores
            if color_primario:
                colores_obj.color_primario = color_primario
            if color_secundario:
                colores_obj.color_secundario = color_secundario
            
            # Guardar (esto disparará el .save() y calculará los campos derivados)
            colores_obj.save()

            return JsonResponse({
                'success': True,
                'message': 'Colores guardados correctamente',
                'municipio_id': municipio_id
            })
        except Municipio.DoesNotExist:
            return JsonResponse({'error': 'Municipio no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)