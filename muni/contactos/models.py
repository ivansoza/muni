from django.db import models

from informacion_municipal.models import Municipio


class Contacto(models.Model):
    """
    Modelo para almacenar información de contacto de un municipio.
    Se relaciona con el modelo Municipio a través de una ForeignKey.
    """
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name='contactos',
        help_text="Municipio al que pertenece este contacto"
    )

    telefono_directo = models.CharField(
        "Teléfono Directo",
        max_length=60,
        blank=True,
        null=True,
        help_text="Número de teléfono directo disponible en horario de oficina"
    )
    correo_electronico = models.EmailField(
        "Correo Electrónico",
        blank=True,
        null=True,
        help_text="Correo electrónico de contacto"
    )
    direccion_oficinas = models.CharField(
        "Dirección de Oficinas",
        max_length=200,
        blank=True,
        null=True,
        help_text="Dirección de las oficinas centrales"
    )
    enlace_mapa = models.CharField(
        "Ver en Mapa",
        max_length=500,

        blank=True,
        null=True,
        help_text="URL de Google Maps u otro servicio de mapas"
    )
    ubicacion = models.CharField(
        "Ubicación",
        max_length=200,
        blank=True,
        null=True,
        help_text="Ubicación escrita (nombre o dirección)"
    )
    horario_servicio = models.CharField(
        "Horario de Servicio",
        max_length=100,
        blank=True,
        null=True,
        help_text="Días y horarios de atención (Ej. Lun-Vie 9:00 AM - 4:00 PM)"
    )

    # Redes Sociales
    facebook = models.URLField(
        "Facebook",
        blank=True,
        null=True,
        help_text="Enlace a la página de Facebook"
    )
    instagram = models.URLField(
        "Instagram",
        blank=True,
        null=True,
        help_text="Enlace a la cuenta de Instagram"
    )
    youtube = models.URLField(
        "YouTube",
        blank=True,
        null=True,
        help_text="Enlace al canal de YouTube"
    )
    tiktok = models.URLField(
        "TikTok",
        blank=True,
        null=True,
        help_text="Enlace a la cuenta de TikTok"
    )

    # Números de emergencia y denuncia anónima
    telefono_emergencia = models.CharField(
        "Número de Emergencias",
        max_length=20,
        default='911',
        help_text="Número de emergencias"
    )
    telefono_denuncia_anonima = models.CharField(
        "Denuncia Anónima",
        max_length=20,
        default='089',
        help_text="Número para denuncias anónimas"
    )

    # Estado y control de actualización
    status = models.CharField(
        "Estado",
        max_length=10,
        choices=STATUS_CHOICES,
        default='activo'
    )
    ultima_actualizacion = models.DateTimeField(
        "Última actualización",
        auto_now=True
    )

    latitud = models.DecimalField(
        "Latitud",
        max_digits=10, 
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Latitud de la ubicación"
    )
    
    longitud = models.DecimalField(
        "Longitud",
        max_digits=10, 
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Longitud de la ubicación"
    )
    # Imagen del contacto
    imagen = models.ImageField(
        "Imagen del Contacto",
        upload_to="contactos/",
        blank=True,
        null=True,
        help_text="Imagen representativa del contacto (opcional)"
    )

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return f"{self.municipio.nombre} - Contacto"
