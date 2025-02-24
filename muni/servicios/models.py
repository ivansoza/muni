from django.db import models
import uuid

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"
    
class Sector(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Sectores"
    
class Dependencia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Dependencias"
    
class Estado(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Estados"
    
class Servicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.ImageField(upload_to='iconos/', null=True, blank=True)  # Permite subir un icono
    url_tramite = models.URLField(null=True, blank=True)
    estado = models.PositiveIntegerField(default=0)  # Número para "+5" en la tarjeta
    clasificacion = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    organismo = models.ForeignKey(Dependencia, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)

    # Nuevos campos para activar/desactivar las opciones
    pago_en_linea = models.BooleanField(default=False)  # Activar o desactivar "Pago en Línea"
    ahora_en_linea = models.BooleanField(default=False)  # Activar o desactivar "Ahora en Línea"

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name_plural = "Servicios"