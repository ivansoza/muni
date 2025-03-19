from django.db import models

from informacion_municipal.models import Municipio
from django.db.models import Q

# Create your models here.





class SocialNetwork(models.Model):
    SOCIAL_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
    ]

    municipio = models.ForeignKey(
        Municipio, 
        on_delete=models.CASCADE, 
        related_name='redes_sociales',
        verbose_name="Municipio"
    )
    social_type = models.CharField(
        "Tipo de Red Social",
        max_length=20,
        choices=SOCIAL_CHOICES
    )
    social_username = models.CharField(
        "Nombre de usuario/identificador",
        max_length=150,
        blank=True,
        null=True
    )
    social_url = models.URLField(
        "URL del perfil",
        max_length=300,
        blank=True,
        null=True
    )
    is_favorite = models.BooleanField(
        "Red favorita",
        default=False,
        help_text="Marcar si es la red social predeterminada"
    )
    fecha_creacion = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True
    )
    fecha_actualizacion = models.DateTimeField(
        "Fecha de actualización",
        auto_now=True
    )

    class Meta:
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        # Restricción para permitir solo una red social favorita por tipo para cada municipio
        constraints = [
            models.UniqueConstraint(
                fields=['municipio', 'social_type'],
                condition=Q(is_favorite=True),
                name='unique_favorite_per_social_type_per_municipio'
            )
        ]

    def __str__(self):
        return f"{self.get_social_type_display()} - {self.social_username}"

    

class ContadorVisitas(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    visitas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Visitas: {self.visitas} - Fecha: {self.fecha}"