from django.db import models
import colorsys

class Municipio(models.Model):
    STATUS_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    nombre_municipio = models.CharField(
        "Nombre Municipio", 
        max_length=120, 
        blank=True, 
        null=True,
        help_text="Nombre Municipio"
    )
    nombre = models.CharField("Nombre oficial", max_length=120, unique=True)

    logotipo = models.ImageField("Logotipo", upload_to='municipio/')
    logotipo_claro = models.ImageField(
        "Logotipo para fondos claros",
        upload_to='municipio/logotipos_claros/',
        blank=True,
        null=True,
        help_text="Versión del logotipo optimizada para fondos claros"
    )
    
    banner = models.ImageField(
        "Banner/Portada", 
        upload_to='municipio/banners/',  
        help_text="Imagen destacada para la página principal"
    )
    descripcion = models.TextField("Descripción breve", max_length=300)
    ultima_actualizacion = models.DateTimeField("Última actualización", auto_now=True)

    status = models.CharField("Estado", max_length=10, choices=STATUS_CHOICES, default='activo')

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return self.nombre


class ColoresMunicipio(models.Model):
    municipio = models.ForeignKey(Municipio, related_name='colores', on_delete=models.CASCADE)
    color_primario = models.CharField("Color primario (HEX)", max_length=7, default='#003366')
    color_secundario = models.CharField("Color secundario (HEX)", max_length=7, default='#FFD700')
    
    # Campos adicionales para almacenar las versiones derivadas
    color_primario_dark = models.CharField("Color primario oscuro (HEX)", max_length=7, blank=True, editable=False)
    color_primario_light = models.CharField("Color primario suave (HEX)", max_length=7, blank=True, editable=False)
    color_secundario_dark = models.CharField("Color secundario oscuro (HEX)", max_length=7, blank=True, editable=False)
    color_secundario_light = models.CharField("Color secundario suave (HEX)", max_length=7, blank=True, editable=False)
    
    # Nuevos campos para almacenar los colores en formato RGB
    color_primario_rgb = models.CharField("Color primario (RGB)", max_length=20, blank=True, editable=False)
    color_secundario_rgb = models.CharField("Color secundario (RGB)", max_length=20, blank=True, editable=False)
    
    # Nuevos campos para almacenar los colores oscuros en formato RGB (sólo números)
    color_primario_dark_rgb = models.CharField("Color primario oscuro (RGB)", max_length=20, blank=True, editable=False)
    color_secundario_dark_rgb = models.CharField("Color secundario oscuro (RGB)", max_length=20, blank=True, editable=False)
    

    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "Paleta de Colores"
        verbose_name_plural = "Paleta de Colores"

    def ajustar_luminosidad(self, hex_color, factor):
        """
        Ajusta la luminosidad del color en formato HEX.
        - factor > 1 para hacer el color más claro.
        - factor < 1 para hacerlo más oscuro.
        """
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convertir a HLS (Hue, Lightness, Saturation)
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        
        # Ajustar luminosidad (manteniendo el mismo tono y saturación)
        l = max(0, min(1, l * factor))
        
        # Convertir de nuevo a RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f'#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}'
    def hex_to_rgb(self, hex_color):
        """
        Convierte un color en formato HEX a una cadena con los números separados por comas.
        Por ejemplo, "#003366" se convertirá en "0,51,102".
        """
        hex_color = hex_color.lstrip('#')
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"{r},{g},{b}"
    
    def save(self, *args, **kwargs):
        # Calcular los colores derivados para el primario
        self.color_primario_dark = self.ajustar_luminosidad(self.color_primario, 0.6)
        self.color_primario_light = self.ajustar_luminosidad(self.color_primario, 1.4)
        # Calcular los colores derivados para el secundario
        self.color_secundario_dark = self.ajustar_luminosidad(self.color_secundario, 0.6)
        self.color_secundario_light = self.ajustar_luminosidad(self.color_secundario, 1.4)
        # Calcular la representación en RGB para los colores base
  
        self.color_primario_rgb = self.hex_to_rgb(self.color_primario)
        self.color_secundario_rgb = self.hex_to_rgb(self.color_secundario)
        # Calcular la representación en RGB para las versiones oscuras
        self.color_primario_dark_rgb = self.hex_to_rgb(self.color_primario_dark)
        self.color_secundario_dark_rgb = self.hex_to_rgb(self.color_secundario_dark)
        
        super().save(*args, **kwargs)  # Factor < 1 = más oscuro

class GobiernoActual(models.Model):
    municipio = models.ForeignKey(Municipio, related_name='gobierno_actual', on_delete=models.CASCADE)
    nombre_alcalde = models.CharField("Alcalde/sa", max_length=150)
    periodo = models.CharField("Período", max_length=9, help_text="Ej: 2024-2025")
    fecha_inicio = models.DateField("Inicio de gestión")
    fecha_fin = models.DateField("Fin de gestión")
    fecha_registro = models.DateTimeField("Fecha de registro", auto_now=True)  # Se actualiza al editar

    class Meta:
        verbose_name = "Gobierno Actual"
        verbose_name_plural = "Gobierno Actual"

class MisionVision(models.Model):
    municipio = models.ForeignKey(Municipio, related_name='mision_vision', on_delete=models.CASCADE)
    mision = models.TextField("Misión", max_length=500)
    vision = models.TextField("Visión", max_length=500)
    valores = models.TextField("Valores", max_length=300, help_text="Separados por comas")
    fecha_actualizacion = models.DateTimeField("Última modificación", auto_now=True)  # Fecha de edición

    class Meta:
        verbose_name = "Misión y Visión"
        verbose_name_plural = "Misión y Visión"



from django.core.exceptions import ValidationError

class SeccionInicio(models.Model):
    OPCIONES_SECCIONES = [
        ('servicios', 'Servicios'),
        ('ultimas_noticias', 'Últimas Noticias'),
        ('convocatorias', 'Convocatorias'),
        ('redes_sociales', 'Redes Sociales'),
        ('contactos', 'Contactos'),
        ('informacion_presidente', 'Información del Presidente'),
        ('dinamica', 'Dinámica'),
    ]
    
    municipio = models.ForeignKey(
        Municipio, 
        on_delete=models.CASCADE,
        verbose_name="Municipio",
        help_text="Selecciona el municipio al que pertenece esta configuración",
        related_name='secciones'
    )
    nombre = models.CharField(
        "Nombre de la sección",
        max_length=50,
        choices=OPCIONES_SECCIONES,
        help_text="Selecciona la sección a mostrar"
    )
    orden = models.PositiveIntegerField(
        "Orden",
        default=0,
        help_text="Número que indica la posición en la página (menor es primero)"
    )
    
    # Campos para secciones dinámicas
    template_dynamic = models.CharField(
         "Template dinámico",
         max_length=255,
         blank=True,
         null=True,
         help_text="Especifica el template a incluir para esta sección dinámica (ej. 'home/components/dinamica.html')"
    )
    contenido_dinamico = models.TextField(
         "Contenido dinámico",
         blank=True,
         null=True,
         help_text="Introduce aquí el HTML completo para la sección dinámica"
    )
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Sección de Inicio"
        verbose_name_plural = "Secciones de Inicio"
    
    def __str__(self):
        return f"{self.get_nombre_display()} (Orden: {self.orden})"
    
    def clean(self):
        """Valida que para secciones estáticas no se repita el mismo tipo para un mismo municipio."""
        if self.nombre != 'dinamica':
            if SeccionInicio.objects.filter(municipio=self.municipio, nombre=self.nombre).exclude(pk=self.pk).exists():
                raise ValidationError(f"Ya existe una sección '{self.get_nombre_display()}' para este municipio.")





