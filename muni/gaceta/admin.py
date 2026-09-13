from django.contrib import admin
from .models import EdicionGaceta


@admin.register(EdicionGaceta)
class EdicionGacetaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'titulo', 'anio', 'fecha_publicacion', 'activo', 'fecha_registro')
    list_filter = ('anio', 'activo')
    search_fields = ('numero', 'titulo', 'descripcion')
    list_editable = ('activo',)
    ordering = ('-anio', '-fecha_publicacion')
    date_hierarchy = 'fecha_publicacion'

    fieldsets = (
        ('Información principal', {
            'fields': ('numero', 'titulo', 'descripcion')
        }),
        ('Fecha y año', {
            'fields': ('anio', 'fecha_publicacion')
        }),
        ('Archivos', {
            'fields': ('archivo', 'portada')
        }),
        ('Publicación', {
            'fields': ('activo',)
        }),
    )
