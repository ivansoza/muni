from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.nombre

class Convocatoria(models.Model):
    ESTADO_CHOICES = [
        ('ABIERTA', 'ABIERTA'),
        ('PRÓXIMA', 'PRÓXIMA'),
        ('CERRADA', 'CERRADA'),
    ]
    
    titulo = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='convocatorias')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='proxima')
    imagen = models.ImageField(upload_to='convocatorias/', null=True, blank=True)
    fecha_apertura = models.DateField()
    fecha_cierre = models.DateField()
    descripcion = models.TextField()
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=False, null=False)  # Ahora usa CKEditor 5    contenido = CKEditor5Field(blank=False, null=False)  # 🔹 Hace que el campo sea requerido
        # Nuevos campos añadidos
    departamento = models.CharField(max_length=255, null=True, blank=True)  # Campo de departamento
    email = models.EmailField(max_length=255, null=True, blank=True)  # Campo de email
    telefono = models.CharField(max_length=15, null=True, blank=True)  # Campo de teléfono
    horarios_atencion = models.CharField(max_length=255, null=True, blank=True)  # Campo de horarios de atención
    def __str__(self):
        return f"{self.titulo} ({self.categoria.nombre} {self.estado})"

class ArchivoConvocatoria(models.Model):
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='convocatorias/archivos/')
    nombre = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre or f"Archivo {self.pk} de {self.convocatoria.titulo}"
