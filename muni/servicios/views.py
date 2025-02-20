from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomeServiciosView(TemplateView):
    template_name = 'homeServicios.html'  # Ruta del template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'servicios'  # Define qué opción está activa

        servicios = [
            {
                "titulo": "Pago de Predial",
                "descripcion": "Mantente al día con el pago de tu impuesto predial sin salir de casa. Realiza tu trámite en línea de manera ágil, segura y sencilla. Solo necesitas ingresar la clave catastral para consultar tu adeudo y efectuar el pago.​",
                "icono": "https://oficialiamayor.sonora.gob.mx/api/icons/inscripcion-registro.svg",
                "url_info": "#",
                "url_tramite": "#",
                "estado": 1
            },
            {
                "titulo": "Pago de Agua Potable",
                "descripcion": "Realiza el pago de tu servicio de agua potable sin complicaciones y desde la comodidad de tu hogar. Solo ingresa tu número de contrato para consultar tu saldo y realiza el pago en unos cuantos pasos.",
                "icono": "https://oficialiamayor.sonora.gob.mx/api/icons/inscripcion-registro.svg",
                "url_info": "#",
                "url_tramite": "#",
                "estado": 2
            },
            {
                "titulo": "Pago de Licencia de Funcionamiento",
                "descripcion": "Facilita el proceso de renovación de tu licencia de funcionamiento sin necesidad de acudir a las oficinas. Consulta el monto correspondiente ingresando los datos de tu negocio y realiza el pago en unos cuantos pasos.​",
                "icono": "https://oficialiamayor.sonora.gob.mx/api/icons/inscripcion-registro.svg",
                "url_info": "#",
                "url_tramite": "#",
                "estado": 3
            },
            {
                "titulo": "Ordenes de pago",
                "descripcion": "Realiza el pago de las órdenes emitidas por el municipio sin complicaciones. Solo necesitas ingresar el número de orden y código de verificación para consultar el importe y efectuar el pago de manera ágil y confiable.",
                "icono": "https://oficialiamayor.sonora.gob.mx/api/icons/inscripcion-registro.svg",
                "url_info": "#",
                "url_tramite": "#",
                "estado": 4
            },
        ]

        # Filtrar por búsqueda
        query = self.request.GET.get('q', '')
        if query:
            servicios = [s for s in servicios if query.lower() in s['titulo'].lower()]

        context['servicios'] = servicios
        return context
