from django.db import models

from informacion_municipal.models import Municipio

class Encuesta(models.Model):
    municipio = models.ForeignKey(
        Municipio, 
        related_name='encuestas', 
        on_delete=models.CASCADE,
        null=True,         # Permite valores nulos en la base de datos
        blank=True         # Permite dejar vacío el campo en formularios
    )
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    encuesta = models.ForeignKey(Encuesta, related_name='preguntas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    orden = models.PositiveIntegerField(default=0, help_text="Define el orden de las preguntas en la encuesta")

    def __str__(self):
        return self.texto


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto


class Envio(models.Model):
    """
    Este modelo representa el envío (o respuesta) completo a una encuesta,
    permitiendo registrar todas las respuestas asociadas a cada pregunta.
    """
    encuesta = models.ForeignKey(Encuesta, related_name='envios', on_delete=models.CASCADE)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Envio {self.id} a {self.encuesta.titulo}"


class Respuesta(models.Model):
    """
    Aquí se guarda la respuesta a una pregunta dentro de un envío.
    Se asume que para cada pregunta se selecciona una opción (radio button).
    """
    envio = models.ForeignKey(Envio, related_name='respuestas', on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, related_name='respuestas', on_delete=models.CASCADE)
    opcion = models.ForeignKey(Opcion, related_name='respuestas', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pregunta.texto} -> {self.opcion.texto}"
import os

class SeccionTransparencia(models.Model):
    """Secciones dinámicas creadas por el usuario"""
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='secciones_imagenes/', blank=True, null=True)  # Campo para imagen
    usa_ejercicios = models.BooleanField(default=False)  # Si permite ejercicios fiscales
    usa_meses = models.BooleanField(default=False)  # Si permite organización por mes

    def __str__(self):
        return self.nombre

class EjercicioFiscal(models.Model):
    """Ejercicio fiscal, que puede abarcar varios años"""
    seccion = models.ForeignKey(SeccionTransparencia, on_delete=models.CASCADE, related_name="ejercicios")
    nombre = models.CharField(max_length=255, blank=True, null=True)  # Nombre del ejercicio (puede ser algo como 'Ejercicio 2024-2025')
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


def ruta_documentos(instance, filename):
    """Genera la ruta de almacenamiento según la estructura de la sección"""
    ext = filename.split('.')[-1]
    filename = f"{instance.titulo}.{ext}"

    # Usar el año y mes directamente desde el modelo DocumentoTransparencia
    if instance.año and instance.mes:
        return os.path.join("transparencia", instance.seccion.nombre, str(instance.año), str(instance.mes), filename)
    elif instance.año:
        return os.path.join("transparencia", instance.seccion.nombre, str(instance.año), filename)
    else:
        return os.path.join("transparencia", instance.seccion.nombre, filename)

class DocumentoTransparencia(models.Model):
    """Almacena documentos dentro de secciones dinámicas"""
    MESES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]
    seccion = models.ForeignKey(SeccionTransparencia, on_delete=models.CASCADE, related_name="documentos")
    ejercicio_fiscal = models.ForeignKey(EjercicioFiscal, on_delete=models.CASCADE, related_name="documentos", null=True, blank=True)  # Nueva relación con EjercicioFiscal
    año = models.PositiveIntegerField(null=True, blank=True)  # Año fiscal directamente como atributo
    mes = models.PositiveSmallIntegerField(choices=MESES, null=True, blank=True)  # Mes con choices
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to=ruta_documentos)
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.seccion.nombre})"

#
    
# Lista de Obligaciones
class ListaObligaciones(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Titulo de la lista')
    articulo = models.CharField(max_length=255, verbose_name='titulo de articulo')

    def __str__(self):
        return f"{self.titulo} - {self.articulo}"

# Artículos de cada lista de obligaciones
class ArticuloLiga(models.Model):
    lista_obligaciones = models.ForeignKey(ListaObligaciones, related_name='articulos_liga', on_delete=models.CASCADE)
    articulo_fraccion = models.CharField(max_length=255, verbose_name='Fracción del articulo')  # Ejemplo: "63" o "63A"
    orden = models.PositiveIntegerField(default=0)  # Campo para definir el orden manualmente
    class Meta:
            ordering = ['orden']  # Los artículos se ordenarán por este campo

    def __str__(self):
        return f"ART. - {self.articulo_fraccion}"


class LigaArchivo(models.Model):
    articuloDe = models.ForeignKey(ArticuloLiga, on_delete=models.CASCADE, verbose_name='Articulo')
    ano = models.PositiveIntegerField(null=True, blank=True, verbose_name='Año')  # Año fiscal directamente como atributo
    liga = models.URLField(blank=True, null=True, verbose_name='link')  # Enlace al artículo completo
    archivo = models.FileField(upload_to='transparencia/documentos/', verbose_name='Archivo', null=True, blank=True)
    def __str__(self):
        return f"ART. - {self.articuloDe} - {self.ano}"

    class Meta:
        ordering = ['-ano'] 
