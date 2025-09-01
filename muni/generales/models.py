import uuid
from django.db import models

from informacion_municipal.models import Municipio
from django.db.models import Q
from django.utils.text import slugify

from convocatorias.models import Categoria

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



class Secciones(models.Model):
    municipio = models.OneToOneField(Municipio, on_delete=models.CASCADE, related_name='secciones_hab')
    noticias = models.BooleanField(default=False)
    convocatorias = models.BooleanField(default=False)
    transparencia = models.BooleanField(default=False)
    servicios = models.BooleanField(default=False)
    habla_con_tus_hijos = models.BooleanField(default=False)
    aviso_de_privacidad = models.BooleanField(default=False)
    gabinete = models.BooleanField(default=False)
    sevac = models.BooleanField(default=False)
    contacts = models.BooleanField(default=False)
    reportes = models.BooleanField(default=False)
    encuestas = models.BooleanField(default=False)
    servicios_en_linea = models.BooleanField(default=False)
    videos = models.BooleanField(default=False)

    def __str__(self):
        return f"Secciones de {self.municipio}"
    




class personalizacionPlantilla(models.Model):
    ENTRADA_CHOICES = [
        ('entrada1', 'Entrada 1'),
        ('entrada2', 'Entrada 2'),
        ('entrada3', 'Entrada 3'),
        ('entrada4', 'Entrada 4'),
        ('sincortina', 'Sin cortina'),
    ]

    municipio = models.OneToOneField(Municipio, on_delete=models.CASCADE, related_name='cortina')
    entrada = models.CharField(
        max_length=50,
        choices=ENTRADA_CHOICES,
        default='entrada1'  # Primera opción como predeterminada
    )
    HERO_CHOICES = [
        ('hero1', 'Hero 1'),
        ('hero2', 'Hero 2'),
        ('hero3', 'Hero 3'),
        ('hero4', 'Hero 4'),
        ('hero5', 'Hero 5'),
        ('sinhero', 'Sin Hero'),
    ]
    hero_seccion = models.CharField(
        max_length=50,
        choices=HERO_CHOICES,
        default='hero1'  # Primera opción como predeterminada
    )

    SERVICIOS_CHOICES = [
        ('servicios1', 'Servicios 1'),
        ('servicios2', 'Servicios 2'),
        ('servicios3', 'Servicios 3'),
        ('servicios4', 'Servicios 4'),
        ('sinservicio', 'Sin Servicio'),
    ]
    servicios = models.CharField(
        max_length=50,
        choices=SERVICIOS_CHOICES,
        default='servicios1'  # Primera opción como predeterminada
    )

    fotografia_servicio = models.ImageField(
        upload_to='fotografias_servicios/',
        blank=True,
        null=True,
        verbose_name="Fotografía servicio"
    )


    CONVOCATORIAS_CHOICES = [
        ('convocatorias1', 'Convocatorias 1'),
        ('convocatorias2', 'Convocatorias 2'),
        ('convocatorias3', 'Convocatorias 3'),
        ('sinconvocatoria', 'Sin Convocatoria'),
    ]
    convocatorias = models.CharField(
        max_length=50,
        choices=CONVOCATORIAS_CHOICES,
        default='convocatorias1'  # Primera opción como predeterminada
    )

    INFO_CHOICES = [
        ('info1', 'Informacion 1'),
        ('info2', 'Informacion 2'),
        ('info3', 'Informacion 3'),
        ('info4', 'Informacion 4'),

        ('sininfo', 'Sin Informacion'),
    ]
    informacion_municipio = models.CharField(
        max_length=50,
        choices=INFO_CHOICES,
        default='info1'  # Primera opción como predeterminada
    )
    ANUNCIOS_CHOICES = [
        ('anuncio1', 'Anuncio 1'),
        ('anuncio2', 'Anuncio 2'),
        ('anuncio3', 'Anuncio 3'),
        ('sinanuncio', 'Sin anuncio'),
    ]

    anuncios = models.CharField(
        max_length=50,
        choices=ANUNCIOS_CHOICES,
        default='sinanuncio',
        verbose_name="Anuncios"
    )

    def __str__(self):
        return f"{self.municipio} - {self.get_entrada_display()}"
    
class MetaMunicipio(models.Model):
    """
    Modelo para almacenar los datos meta de cada Municipio
    (etiquetas meta, Open Graph, etc.)
    """
    municipio = models.OneToOneField(
        Municipio,
        on_delete=models.CASCADE,
        related_name='meta'
    )

    # Etiquetas meta básicas
    meta_title = models.CharField(
        max_length=255,
        default='Gobierno Municipal - Inicio',
        help_text="Título para la etiqueta <title> y meta title"
    )
    meta_description = models.TextField(
        default='Descripción breve del municipio para SEO.',
        help_text="Contenido de la etiqueta meta description"
    )
    meta_keywords = models.CharField(
        max_length=255,
        default='Municipio, Gobierno, Servicios',
        help_text="Palabras clave para la etiqueta meta keywords"
    )

    # Open Graph (Facebook, LinkedIn, etc.)
    og_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Título para compartir en redes sociales (og:title)."
    )
    og_description = models.TextField(
        blank=True,
        help_text="Descripción para compartir en redes sociales (og:description)."
    )
    # Este campo puede almacenar la URL de la imagen
    # o, si deseas, un ImageField que luego se sirva como og:image
    og_image = models.ImageField(
        upload_to='og_images/',
        null=True,
        blank=True,
        help_text="Imagen que se mostrará al compartir (og:image)."
    )

    # Twitter Cards (opcional)
    twitter_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Título para Twitter Card."
    )
    twitter_description = models.TextField(
        blank=True,
        help_text="Descripción para Twitter Card."
    )
    twitter_image = models.ImageField(
        upload_to='twitter_images/',
        null=True,
        blank=True,
        help_text="Imagen para Twitter Card."
    )

    def __str__(self):
        return f"MetaMunicipio de {self.municipio.nombre}"

    def get_og_image_url(self):
        """
        Retorna la URL de la imagen OG si existe.
        En caso contrario, intenta usar el logotipo del Municipio.
        Si tampoco existe logotipo, retorna un path/URL por defecto.
        """
        if self.og_image:
            return self.og_image.url
        elif self.municipio.logotipo:
            return self.municipio.logotipo.url
        # URL estática de respaldo si no hay ninguna imagen
        return '/static/assets/images/logo/logo-new.png'
    
class SeccionPlus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categoria_convocatoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='secciones_plus',
        null=True,        # permite valor NULL en la BD
        blank=True        # permite dejarlo en blanco en formularios/admin
    )
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name='secciones_plus'
    )
    nombre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    banner = models.ImageField(
        upload_to='banners_secciones/',
        blank=True,
        null=True
    )
    status = models.BooleanField(default=True)

    incluye_recomendaciones = models.BooleanField(
        default=False,
        help_text="Marcar si esta sección debe mostrar recomendaciones."
    )

    detalles = models.TextField(
        blank=True,
        null=True,
        help_text="Campo opcional para agregar detalles adicionales de la sección."
    )
    es_general = models.BooleanField(
        default=False,
        help_text="Marcar si esta sección es de tipo general."
    )
    archivo = models.FileField(
        upload_to='archivos_secciones/',
        blank=True,
        null=True,
        help_text="Archivo opcional relacionado con la sección."
    )
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class SeccionPlusArchivo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relación muchos-a-uno: varios archivos por SeccionPlus
    seccion = models.ForeignKey(
        SeccionPlus,
        on_delete=models.CASCADE,
        related_name='archivos'  # seccion.archivos.all()
    )

    descripcion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descripción breve del archivo."
    )

    archivo = models.FileField(
        upload_to='archivos_seccion_plus/',
        help_text="Archivo relacionado a la sección."
    )

    def __str__(self):
        return self.descripcion or f'Archivo {self.pk} de {self.seccion.nombre}'


class Recomendaciones(models.Model):
    municipio = models.ForeignKey(
        Municipio,
        related_name='recomendaciones',  
        on_delete=models.CASCADE
    )
    area = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recomendación - {self.area} ({self.municipio})"


class ArchivoRelacionadoRecomendacion(models.Model):
    recomendacion = models.ForeignKey(
        Recomendaciones,
        related_name='archivos_relacionados',  # podrás hacer recomendacion.archivos_relacionados.all()
        on_delete=models.CASCADE
    )
    archivo = models.FileField(
        upload_to='archivos_recomendaciones/', 
        blank=False, 
        null=False
    )
    descripcion = models.CharField(
        max_length=255, 
        blank=True, 
        null=True
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archivo: {self.descripcion or 'Sin descripción'}"




class VideoMunicipio(models.Model):
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name='videos'      # aquí definimos el related_name
    )
    nombre = models.CharField(max_length=255, verbose_name='Título')
    frame = models.URLField(verbose_name='URL o frame de YouTube')
    orden = models.PositiveIntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['orden']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.nombre
    