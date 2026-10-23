from django.db import models
from django.core.exceptions import ValidationError
import os


def validar_pdf(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.pdf':
        raise ValidationError('Solo se permiten archivos PDF.')


class EdicionGaceta(models.Model):
    numero = models.CharField(
        max_length=50,
        verbose_name='Número de edición',
        help_text='Ej: 001, 2024-01'
    )
    titulo = models.CharField(
        max_length=255,
        verbose_name='Título',
        help_text='Ej: Gaceta Municipal No. 1 – Enero 2024'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Resumen breve del contenido de esta edición'
    )
    anio = models.PositiveIntegerField(verbose_name='Año')
    fecha_publicacion = models.DateField(verbose_name='Fecha de publicación')
    archivo = models.FileField(
        upload_to='gaceta/ediciones/',
        verbose_name='Archivo PDF',
        validators=[validar_pdf]
    )
    portada = models.ImageField(
        upload_to='gaceta/portadas/',
        blank=True,
        null=True,
        verbose_name='Imagen de portada',
        help_text='Imagen opcional que representa la portada de la edición'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Visible al público',
        help_text='Desactiva para ocultar esta edición sin eliminarla'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Edición de Gaceta Municipal'
        verbose_name_plural = 'Ediciones de Gaceta Municipal'
        ordering = ['-anio', '-fecha_publicacion']

    def __str__(self):
        return f'Gaceta No. {self.numero} – {self.anio}'

    @property
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name)