from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=False, null=False)  # Ahora usa CKEditor 5    contenido = CKEditor5Field(blank=False, null=False)  # 🔹 Hace que el campo sea requerido
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="noticias")
    imagen = models.ImageField(upload_to='noticias/imagenes/', blank=True)

class ImagenGaleria(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='imagenes_galeria', null=True, blank=True)  # 👈 Aquí está la clave
    imagen = models.ImageField(upload_to='noticias/galeria/')