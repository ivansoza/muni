from django.contrib import admin

# Register your models here.
from .models import Noticia, ImagenGaleria, Categoria

admin.site.register(Noticia)
admin.site.register(ImagenGaleria)
admin.site.register(Categoria)