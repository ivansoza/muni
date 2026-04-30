from django.contrib import admin
from .models import Categoria, Autor, Articulo, Comentario, Like, VideoArticulo
# Register your models here.

admin.site.register(Categoria)
admin.site.register(Autor)
admin.site.register(Articulo)
admin.site.register(Comentario)
admin.site.register(Like)
admin.site.register(VideoArticulo)

from .models import SeccionHistoria

@admin.register(SeccionHistoria)
class SeccionHistoriaAdmin(admin.ModelAdmin):
    list_display = ('get_rubro_display', 'titulo', 'orden', 'activo', 'fecha_actualizacion')
    list_editable = ('orden', 'activo')
    list_filter = ('activo', 'rubro')
    ordering = ('orden',)