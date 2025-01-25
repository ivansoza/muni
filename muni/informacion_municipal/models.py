from django.db import models



class DatosMunicipio(models.Model):
    nombre = models.CharField("Nombre oficial", max_length=120, unique=True)
    logotipo = models.ImageField("Logotipo", upload_to='municipio/')
    banner = models.ImageField(
        "Banner/Portada", 
        upload_to='municipio/banners/',  # Carpeta específica para banners
        help_text="Imagen destacada para la página principal"
    )
    descripcion = models.TextField("Descripción breve", max_length=300)
    ultima_actualizacion = models.DateTimeField("Última actualización", auto_now=True)

    class Meta:
        verbose_name = "Datos Municipales"
        verbose_name_plural = "Datos Municipales"

    def __str__(self):
        return self.nombre
    
class ColoresMunicipio(models.Model):
    color_primario = models.CharField("Color primario (HEX)", max_length=7, default='#003366')
    color_secundario = models.CharField("Color secundario (HEX)", max_length=7, default='#FFD700')
    color_terciario = models.CharField("Color terciario (HEX)", max_length=7, default='#FFFFFF')
    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)  # Fecha de registro inicial

    class Meta:
        verbose_name = "Paleta de Colores"
        verbose_name_plural = "Paleta de Colores"

class GobiernoActual(models.Model):
    nombre_alcalde = models.CharField("Alcalde/sa", max_length=150)
    periodo = models.CharField("Período", max_length=9, help_text="Ej: 2024-2025")
    fecha_inicio = models.DateField("Inicio de gestión")
    fecha_fin = models.DateField("Fin de gestión")
    fecha_registro = models.DateTimeField("Fecha de registro", auto_now=True)  # Se actualiza al editar

    class Meta:
        verbose_name = "Gobierno Actual"
        verbose_name_plural = "Gobierno Actual"

class MisionVision(models.Model):
    mision = models.TextField("Misión", max_length=500)
    vision = models.TextField("Visión", max_length=500)
    valores = models.TextField("Valores", max_length=300, help_text="Separados por comas")
    fecha_actualizacion = models.DateTimeField("Última modificación", auto_now=True)  # Fecha de edición

    class Meta:
        verbose_name = "Misión y Visión"
        verbose_name_plural = "Misión y Visión"