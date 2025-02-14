from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = CKEditor5Field('Contenido', config_name='extends')  # Ahora usa CKEditor 5
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="noticias")
    imagen = models.ImageField(upload_to='noticias/imagenes/')
    imagenes_galeria = models.ManyToManyField('ImagenGaleria', blank=True)

class ImagenGaleria(models.Model):
    imagen = models.ImageField(upload_to='noticias/galeria/')