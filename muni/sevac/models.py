from django.db import models
import os
from django.utils.text import slugify

class CategoriaSevac(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Carpeta(models.Model):
    ESTATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey(CategoriaSevac, on_delete=models.SET_NULL, null=True, blank=True)
    padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcarpetas',
        on_delete=models.CASCADE
    )
    estatus = models.CharField(max_length=1, choices=ESTATUS_CHOICES, default='A')  # Campo de estatus

    class Meta:
        unique_together = ('nombre', 'padre')

    def __str__(self):
        return f"{self.nombre}" if not self.padre else f"{self.padre}/{self.nombre}"

    def ruta_completa(self):
        if self.padre:
            return f"{self.padre.ruta_completa()}/{slugify(self.nombre)}"
        return slugify(self.nombre)
    
def archivo_upload_to(instance, filename):
    nombre_archivo, extension = os.path.splitext(filename)
    slug = slugify(nombre_archivo)
    return f'sevac/{instance.carpeta.ruta_completa()}/{slug}{extension}'

class Archivo(models.Model):
    ESTATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]

    carpeta = models.ForeignKey(Carpeta, related_name='archivos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to=archivo_upload_to)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=1, choices=ESTATUS_CHOICES, default='A')  # Campo de estatus

    def __str__(self):
        return self.nombre
