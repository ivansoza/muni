from django.db import models

from informacion_municipal.models import Municipio
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class AvisoDePrivacidad(models.Model):
    municipio = models.ForeignKey(Municipio, related_name='avisos_privacidad', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=False, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aviso de Privacidad - {self.titulo} ({self.municipio})"


# Modelo para Archivos Relacionados
class ArchivoRelacionado(models.Model):
    aviso_privacidad = models.ForeignKey(AvisoDePrivacidad, related_name='archivos_relacionados', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='archivos_avisos/', blank=False, null=False)  # Campo para subir archivos
    descripcion = models.CharField(max_length=255, blank=True, null=True)  # Descripción del archivo
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archivo: {self.descripcion if self.descripcion else 'Sin descripción'}"
