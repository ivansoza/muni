from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=225, unique=True, verbose_name='Nombre de la categoría')
    def __str__(self):
        return self.nombre
    
class Autor(models.Model):
    nombre_completo = models.CharField(max_length=300, verbose_name='Nombre completo')
    perfil = models.CharField(max_length=225, verbose_name='Perfil del autor')
    trayectoria = models.TextField()
    fotografia = models.ImageField(upload_to='fotografias/', verbose_name='Fotografía del autor')
    def __str__(self):
        return f"{self.nombre_completo} - {self.perfil}"

class Articulo(models.Model):
    titulo = models.CharField(max_length=255, verbose_name='Titulo del articulo')
    abstract = models.TextField()
    contenido = CKEditor5Field('Contenido', config_name='extends', blank=False, null=False)  
    imagen = models.ImageField(upload_to='habla_con_tus_hijos/imagenes/', verbose_name='Imagen principal')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoría')  # Usamos ForeignKey en lugar de ManyToMany
    etiquetas = models.CharField(max_length=225, verbose_name='Etiquetas del articulo', blank=True, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, verbose_name='Autor del articulo', blank=True, null=True)
    destacado = models.BooleanField(default=False)
    tiempo_lectura = models.PositiveIntegerField(default=1, verbose_name='Tiempo estimado de lectura')  # Tiempo en minutos
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)  # Contador de likes
    habla = models.BooleanField(default=False, verbose_name= "Habla con tus hijos")
    ven_vive = models.BooleanField(default=False, verbose_name= "Ven vive y vuelve a tu municipio")
    video_url = models.URLField(
        verbose_name='Enlace de video',
        max_length=500,
        blank=True,
        null=True,
        help_text='URL de un video relacionado, por ejemplo de YouTube o Vimeo.'
    )
    def dar_like(self, ip_address):
        # Verifica si la IP ya ha dado like
        if not Like.objects.filter(articulo=self, ip_address=ip_address).exists():
            self.likes += 1
            self.save()
            # Guarda el like con la IP
            Like.objects.create(articulo=self, ip_address=ip_address)

    def __str__(self):
        return f'{self.titulo} - {self.autor} - {self.fecha_publicacion}' 
    
class Like(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'Like de {self.ip_address} en {self.articulo.titulo}'

class Comentario(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='comentarios')
    nombre = models.CharField(max_length=255, blank=True, null=True)  # Nombre opcional del comentarista
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    respuesta = models.BooleanField(default=False, verbose_name='¿Es una respuesta?')

    def __str__(self):
        return f'Comentario de {self.nombre or "Anónimo"} en {self.articulo.titulo}'

