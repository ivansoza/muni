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

class CanalPresentacion(models.Model):
    nombre = models.CharField(
        max_length=50,
        choices=[
            ("presencial", "Presencial"),
            ("linea", "En Línea"),
            ("mixto", "Presencial y En Línea")
        ],
        unique=True
    )

    def __str__(self):
        return self.get_nombre_display()
    
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
    responsable = models.ForeignKey('gobierno.MiembroGabinete', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name_plural = "Servicios"

class EnQueConsiste(models.Model):
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name="detalle")
    tramite = models.CharField(max_length=255, choices=[("Tiene Costo", "Tiene Costo"), ("Sin Costo", "Sin Costo")], default="Sin Costo")
    canal_presentacion = models.ForeignKey(CanalPresentacion, on_delete=models.PROTECT)
    solicitado_por = models.CharField(max_length=255, choices=[("Persona física", "Persona física"), ("Persona moral", "Persona moral"), ("Ambos", "Persona Física y Moral")], default="Ambos")
    momento_solicitud = models.CharField(max_length=255, default="En cualquier momento")

    def __str__(self):
        return f"Detalle de {self.servicio.titulo}"
    
    class Meta:
        verbose_name_plural = "1. ¿En que consiste?"

class QueSeRequiere(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="requisitos")
    nombre = models.CharField(max_length=255)  # Nombre del documento
    especificaciones = models.TextField(default="N/A")  # Descripción del requisito
    tipo_documento = models.TextField(default="N/A")
    presentar_original = models.PositiveIntegerField(default=0)  # Número de originales requeridos
    presentar_copia = models.PositiveIntegerField(default=0)  # Número de copias requeridas
    archivo_descarga = models.FileField(upload_to="requisitos/", null=True, blank=True)  # Archivo descargable opcional

    def __str__(self):
        return f"{self.nombre} - {self.servicio.titulo}"
    
    class Meta:
        verbose_name_plural = "2. ¿Que se requiere?"

class ComoLoRealizo(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='instrucciones')
    canal_presentacion = models.ForeignKey(CanalPresentacion, on_delete=models.PROTECT)
    paso = models.PositiveIntegerField()
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.servicio.titulo} - {self.canal_presentacion} - {self.paso}"
    
    class Meta:
        verbose_name_plural = "3. ¿Como lo realizo?"

class CuantoCuesta(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='costos')
    concepto = models.CharField(max_length=255)
    notas = models.TextField(blank=True, null=True)
    vigencia = models.CharField(max_length=100, default="Sin vigencia")
    tipo = models.CharField(max_length=100, default="Variable")
    costo = models.CharField(max_length=100, help_text="Ej. $200.00 o Entre $200 y $500")
    momento_pago = models.CharField(max_length=255, default="Al solicitar el trámite")

    def __str__(self):
        return f"{self.servicio.titulo} - {self.concepto}"
    
    class Meta:
        verbose_name_plural = "4. ¿Cuánto cuesta?"