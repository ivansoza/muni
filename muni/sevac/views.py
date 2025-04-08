from django.shortcuts import render
from .models import Carpeta, Archivo
from django.views.generic import TemplateView
from collections import defaultdict

class HomeSevacView(TemplateView):
    template_name = 'archivosListas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener las carpetas principales activas
        carpetas = Carpeta.objects.filter(padre=None, estatus='A')

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
        carpetas_ordenadas = sorted(carpetas, key=ordenar_carpetas)

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

        # Agrupar carpetas por objeto categoria
        categorias = defaultdict(list)
        for carpeta in carpetas_ordenadas:
            if carpeta.categoria:
                categorias[carpeta.categoria].append(carpeta)

        # Añadir las carpetas ordenadas al contexto
        context['carpetas'] = carpetas_ordenadas
        context['categorias'] = dict(categorias)
        context['sidebar'] = "sevac"

        return context

