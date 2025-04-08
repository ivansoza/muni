from django.shortcuts import render
from .models import Carpeta, Archivo, CategoriaSevac
from django.views.generic import TemplateView

class HomeSevacView(TemplateView):
    template_name = 'archivosListas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria_id = self.request.GET.get('categoria')

        # Obtener las carpetas principales activas
        carpetas_qs = Carpeta.objects.filter(padre=None, estatus='A').select_related('categoria')

        if categoria_id:
            carpetas_qs = carpetas_qs.filter(categoria__id=categoria_id)

        # Ordenar carpetas según los criterios especificados
        def ordenar_carpetas(carpeta):
            nombre = carpeta.nombre
            # Detectar si el nombre contiene números
            if nombre.isdigit():
                # Convertir a entero para ordenar por número
                return (-int(nombre), nombre)  # Ordenar números de mayor a menor
            else:
                # Si contiene letras, devolver una clave que las coloque después de los números
                return (0, nombre.lower())  # Orden alfabético para letras

        # Aplicar el orden a las carpetas principales
        carpetas_ordenadas = sorted(carpetas_qs, key=ordenar_carpetas)

        # Ordenar recursivamente las subcarpetas
        def ordenar_subcarpetas(carpeta):
            subcarpetas = list(carpeta.subcarpetas.filter(estatus='A'))
            subcarpetas_ordenadas = sorted(subcarpetas, key=ordenar_carpetas)
            for subcarpeta in subcarpetas_ordenadas:
                # Ordenar recursivamente las subcarpetas dentro de las subcarpetas
                subcarpeta.subcarpetas_ordenadas = ordenar_subcarpetas(subcarpeta)
            return subcarpetas_ordenadas

        # Agregar las subcarpetas ordenadas a cada carpeta principal
        for carpeta in carpetas_ordenadas:
            carpeta.subcarpetas_ordenadas = ordenar_subcarpetas(carpeta)

        # Añadir las carpetas ordenadas al contexto
        context['carpetas'] = carpetas_ordenadas
        context['categorias'] = CategoriaSevac.objects.all()
        context['categoria_seleccionada'] = int(categoria_id) if categoria_id else None
        context['sidebar'] = "sevac"

        return context

