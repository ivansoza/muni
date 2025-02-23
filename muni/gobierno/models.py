from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from informacion_municipal.models import Municipio

# Create your models here.

class MiembroGabinete(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    municipio = models.ForeignKey(
        Municipio, 
        on_delete=models.CASCADE, 
        related_name="gabinete",
        verbose_name="Municipio"
    )
    nombre = models.CharField("Nombre", max_length=255)
    cargo = models.CharField("Cargo", max_length=255)
    semblanza = CKEditor5Field('Semblanza', config_name='extends', blank=True, null=True)
    numero_contacto = models.CharField("Número de Contacto", max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField("Correo Electrónico", blank=True, null=True)
    pagina_web = models.URLField("Página Web", blank=True, null=True)
    
    # Nuevo campo para almacenar la foto
    imagen = models.ImageField(
        "Fotografía del Miembro",
        upload_to='gabinete/',
        blank=True,
        null=True,
        help_text="Carga la fotografía del miembro (opcional)."
    )
    
    orden = models.PositiveIntegerField(
        "Orden", 
        default=1, 
        help_text="El miembro con orden 1 será considerado el principal."
    )
    status = models.CharField(
        "Estado", 
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='activo'
    )

    class Meta:
        ordering = ['orden']
        verbose_name = "Miembro del Gabinete"
        verbose_name_plural = "Miembros del Gabinete"

    def __str__(self):
        return f"{self.orden} - {self.nombre} ({self.cargo})"
