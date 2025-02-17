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
