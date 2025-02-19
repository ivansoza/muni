from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import SeccionTransparencia
from django.shortcuts import get_object_or_404
from .models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia
from collections import defaultdict
import json  # Para visualizar los datos en la consola

# Create your views here.
class HomeTransparenciaView(TemplateView):
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


