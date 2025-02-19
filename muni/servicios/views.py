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
                "titulo": "Revalidación de placas para el ejercicio 2025",
                "descripcion": "El perro (Canis familiaris o Canis lupus familiaris, dependiendo de si se lo considera una especie o una subespecie del lobo),1​2​3​ llamado perro doméstico o can,4​ y en algunos lugares coloquialmente llamado chucho,5​ tuso,6​ choco,7​ entre otros; es un mamífero carnívoro de la familia de los cánidos, que constituye una especie del género Canis.8​9​ En el 2013, la población mundial estimada de perros estaba entre setecientos millones y novecientos ochenta y siete millones.10​11​",
                "icono": "https://oficialiamayor.sonora.gob.mx/api/icons/inscripcion-registro.svg",
                "url_info": "#",
                "url_tramite": "#",
                "estado": 1
            },
            {
                "titulo": "Expedición de copia certificada de actas",
                "descripcion": "Registro Civil del Estado",
                "icono": "https://oficialiamayor.sonora.gob.mx/api/icons/inscripcion-registro.svg",
                "url_info": "#",
                "url_tramite": "#",
                "estado": 2
            },
            {
                "titulo": "Revalidación de placas para el ejercicio 2025",
                "descripcion": "El perro (Canis familiaris o Canis lupus familiaris, dependiendo de si se lo considera una especie o una subespecie del lobo),1​2​3​ llamado perro doméstico o can,4​ y en algunos lugares coloquialmente llamado chucho,5​ tuso,6​ choco,7​ entre otros; es un mamífero carnívoro de la familia de los cánidos, que constituye una especie del género Canis.8​9​ En el 2013, la población mundial estimada de perros estaba entre setecientos millones y novecientos ochenta y siete millones.10​11​",
                "icono": "https://oficialiamayor.sonora.gob.mx/api/icons/inscripcion-registro.svg",
                "url_info": "#",
                "url_tramite": "#",
                "estado": 3
            },
            {
                "titulo": "Expedición de copia certificada de actas",
                "descripcion": "Registro Civil del Estado",
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
