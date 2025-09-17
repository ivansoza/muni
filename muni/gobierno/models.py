from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from informacion_municipal.models import Municipio
from servicios.models import Dependencia
from django.conf import settings   # 👈 para AUTH_USER_MODEL

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
    semblanza = models.TextField("Semblanza", blank=True, null=True)
    numero_contacto = models.CharField("Número de Contacto", max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField("Correo Electrónico", blank=True, null=True)
    pagina_web = models.URLField("Página Web", blank=True, null=True)
    
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
    
    # Nuevos campos:
    telefono = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    horario = models.CharField("Horario de Atención", max_length=255, blank=True, null=True)
    formacion_academica = models.TextField("Formación Académica", blank=True, null=True)
    experiencia = models.TextField("Experiencia en el Servicio Público", blank=True, null=True)
    area = models.CharField("Área de Trabajo", max_length=255, blank=True, null=True)
    descripcion_area = models.TextField("Descripción del Área de Trabajo", blank=True, null=True)
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=True, null=True)

    # Relación con Dependencia
    dependencia = models.ForeignKey(
        Dependencia, 
        on_delete=models.CASCADE, 
        related_name="miembros", 
        verbose_name="Dependencia",
        blank=True,  # Permite que este campo quede vacío en formularios
        null=True    # Permite que este campo sea nulo en la base de datos
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="miembros_gabinete", blank=True, null=True
    )

    class Meta:
        ordering = ['orden']
        verbose_name = "Miembro del Gabinete"
        verbose_name_plural = "Miembros del Gabinete"

    def __str__(self):
        return f"{self.orden} - {self.nombre} ({self.cargo})"



class MiembroGabineteRegidores(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    municipio = models.ForeignKey(
        Municipio, 
        on_delete=models.CASCADE, 
        related_name="gabinete_regidores",
        verbose_name="Municipio"
    )
    nombre = models.CharField("Nombre", max_length=255)
    cargo = models.CharField("Cargo", max_length=255)
    semblanza = models.TextField("Semblanza", blank=True, null=True)
    numero_contacto = models.CharField("Número de Contacto", max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField("Correo Electrónico", blank=True, null=True)
    pagina_web = models.URLField("Página Web", blank=True, null=True)
    
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
    
    # Nuevos campos:
    telefono = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    horario = models.CharField("Horario de Atención", max_length=255, blank=True, null=True)
    formacion_academica = models.TextField("Formación Académica", blank=True, null=True)
    experiencia = models.TextField("Experiencia en el Servicio Público", blank=True, null=True)
    area = models.CharField("Área de Trabajo", max_length=255, blank=True, null=True)
    descripcion_area = models.TextField("Descripción del Área de Trabajo", blank=True, null=True)
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=True, null=True)

    # Relación con Dependencia
    dependencia = models.ForeignKey(
        Dependencia, 
        on_delete=models.CASCADE, 
        related_name="miembros_regidores", 
        verbose_name="Dependencia",
        blank=True,  # Permite que este campo quede vacío en formularios
        null=True    # Permite que este campo sea nulo en la base de datos
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="miembros_regidores", blank=True, null=True
    )
    class Meta:
        ordering = ['orden']
        verbose_name = "Miembro del Gabinete"
        verbose_name_plural = "Miembros del Gabinete"

    def __str__(self):
        return f"{self.orden} - {self.nombre} ({self.cargo})"



class MiembroGabineteDirectores(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    municipio = models.ForeignKey(
        Municipio, 
        on_delete=models.CASCADE, 
        related_name="gabinete_directores",
        verbose_name="Municipio"
    )
    nombre = models.CharField("Nombre", max_length=255)
    cargo = models.CharField("Cargo", max_length=255)
    semblanza = models.TextField("Semblanza", blank=True, null=True)
    numero_contacto = models.CharField("Número de Contacto", max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField("Correo Electrónico", blank=True, null=True)
    pagina_web = models.URLField("Página Web", blank=True, null=True)
    
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
    
    # Nuevos campos:
    telefono = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    horario = models.CharField("Horario de Atención", max_length=255, blank=True, null=True)
    formacion_academica = models.TextField("Formación Académica", blank=True, null=True)
    experiencia = models.TextField("Experiencia en el Servicio Público", blank=True, null=True)
    area = models.CharField("Área de Trabajo", max_length=255, blank=True, null=True)
    descripcion_area = models.TextField("Descripción del Área de Trabajo", blank=True, null=True)
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=True, null=True)
  
    # Relación con Dependencia
    dependencia = models.ForeignKey(
        Dependencia, 
        on_delete=models.CASCADE, 
        related_name="miembros_directores", 
        verbose_name="Dependencia",
        blank=True,  # Permite que este campo quede vacío en formularios
        null=True    # Permite que este campo sea nulo en la base de datos
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="miembros_directores", blank=True, null=True
    )
    class Meta:
        ordering = ['orden']
        verbose_name = "Miembro del Gabinete"
        verbose_name_plural = "Miembros del Gabinete"

    def __str__(self):
        return f"{self.orden} - {self.nombre} ({self.cargo})"
    

class MiembroGabinetePresidentesComu(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name="gabinete_presidentes_comu",
        verbose_name="Municipio"
    )
    nombre = models.CharField("Nombre", max_length=255)
    cargo = models.CharField("Cargo", max_length=255)
    semblanza = models.TextField("Semblanza", blank=True, null=True)
    numero_contacto = models.CharField("Número de Contacto", max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField("Correo Electrónico", blank=True, null=True)
    pagina_web = models.URLField("Página Web", blank=True, null=True)
    
    imagen = models.ImageField(
        "Fotografía del Presidente Comunal",
        upload_to='presidentes_comu/',
        blank=True,
        null=True,
        help_text="Carga la fotografía del presidente comunal (opcional)."
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
    
    # Nuevos campos:
    telefono = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    horario = models.CharField("Horario de Atención", max_length=255, blank=True, null=True)
    formacion_academica = models.TextField("Formación Académica", blank=True, null=True)
    experiencia = models.TextField("Experiencia en el Servicio Público", blank=True, null=True)
    area = models.CharField("Área de Trabajo", max_length=255, blank=True, null=True)
    descripcion_area = models.TextField("Descripción del Área de Trabajo", blank=True, null=True)
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=True, null=True)
    dependencia = models.ForeignKey(
        Dependencia,
        on_delete=models.CASCADE,
        related_name="presidentes_comu",
        verbose_name="Dependencia",
        blank=True,
        null=True
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="miembros_presidentes_comu", blank=True, null=True
    )


    class Meta:
        ordering = ['orden']
        verbose_name = "Miembro del Gabinete / Presidente Comunal"
        verbose_name_plural = "Miembros del Gabinete / Presidentes Comunales"

    def __str__(self):
        return f"{self.orden} - {self.nombre} ({self.cargo})"
    

class MiembroGabineteCoordinadoresDif(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,
        related_name="gabinete_coordinadores_dif",
        verbose_name="Municipio"
    )
    nombre = models.CharField("Nombre", max_length=255)
    cargo = models.CharField("Cargo", max_length=255)
    semblanza = models.TextField("Semblanza", blank=True, null=True)
    numero_contacto = models.CharField("Número de Contacto", max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField("Correo Electrónico", blank=True, null=True)
    pagina_web = models.URLField("Página Web", blank=True, null=True)
    
    imagen = models.ImageField(
        "Fotografía del Coordinador DIF",
        upload_to='coordinadores_dif/',
        blank=True,
        null=True,
        help_text="Carga la fotografía del coordinador/a DIF (opcional)."
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
    
    # Nuevos campos:
    telefono = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    horario = models.CharField("Horario de Atención", max_length=255, blank=True, null=True)
    formacion_academica = models.TextField("Formación Académica", blank=True, null=True)
    experiencia = models.TextField("Experiencia en el Servicio Público", blank=True, null=True)
    area = models.CharField("Área de Trabajo", max_length=255, blank=True, null=True)
    descripcion_area = models.TextField("Descripción del Área de Trabajo", blank=True, null=True)
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=True, null=True)
    dependencia = models.ForeignKey(
        Dependencia,
        on_delete=models.CASCADE,
        related_name="coordinadores_dif",
        verbose_name="Dependencia",
        blank=True,
        null=True
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name="miembros_coordinadores_dif", blank=True, null=True
    )

    class Meta:
        ordering = ['orden']
        verbose_name = "Miembro del Gabinete / Coordinador DIF"
        verbose_name_plural = "Miembros del Gabinete / Coordinadores DIF"

    def __str__(self):
        return f"{self.orden} - {self.nombre} ({self.cargo})"