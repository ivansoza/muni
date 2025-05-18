from django.contrib import admin
from .models import Categoria, Autor, Articulo, Comentario, Like
# Register your models here.

admin.site.register(Categoria)
admin.site.register(Autor)
admin.site.register(Articulo)
admin.site.register(Comentario)
admin.site.register(Like)