from django.contrib import admin
from .models import DatosMunicipio, ColoresMunicipio, GobiernoActual, MisionVision
from django.utils.html import format_html

@admin.register(DatosMunicipio)
class DatosMunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ultima_actualizacion', 'preview_logotipo', 'preview_banner')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('ultima_actualizacion',)
    readonly_fields = ('preview_logotipo', 'preview_banner', 'ultima_actualizacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Elementos Visuales', {
            'fields': (
                ('logotipo', 'preview_logotipo'),
                ('banner', 'preview_banner')
            ),
            'classes': ('collapse',),
            'description': 'Formatos recomendados: PNG para logos (200x200px), JPG para banners (1920x1080px)'
        }),
        ('Metadata', {
            'fields': ('ultima_actualizacion',),
            'classes': ('collapse',)
        })
    )

    # Vista previa del logotipo (mejorada)
    def preview_logotipo(self, obj):
        if obj.logotipo:
            return format_html(
                '<div style="border: 1px solid #ddd; padding: 5px; display: inline-block">'
                '<img src="{}" style="max-height: 60px; max-width: 120px; object-fit: contain"/>'
                '</div>',
                obj.logotipo.url
            )
        return "-"
    preview_logotipo.short_description = 'Logo Actual'

    # Vista previa del banner (mejorada)
    def preview_banner(self, obj):
        if obj.banner:
            return format_html(
                '<div style="border: 1px solid #ddd; margin: 5px 0">'
                '<img src="{}" style="max-height: 100px; width: 250px; object-fit: cover"/>'
                '</div>',
                obj.banner.url
            )
        return "-"
    preview_banner.short_description = 'Banner Actual'

from django.utils.html import format_html
from django.contrib import admin
from .models import ColoresMunicipio

@admin.register(ColoresMunicipio)
class ColoresMunicipioAdmin(admin.ModelAdmin):
    # Campos REALES editables (deben estar en list_display)
    list_editable = ("color_primario", "color_secundario", "color_terciario")
    
    # list_display incluye los campos editables + métodos visuales
    list_display = (
        "muestra_color_primario",
        "color_primario",  # <--- Campo real incluido
        "muestra_color_secundario",
        "color_secundario",  # <--- Campo real incluido
        "muestra_color_terciario",
        "color_terciario",  # <--- Campo real incluido
        "fecha_creacion",
    )
    
    # Ocultar los títulos de los campos reales
    def color_primario(self, obj):
        return ""  # Devuelve un string vacío
    
    def color_secundario(self, obj):
        return ""
    
    def color_terciario(self, obj):
        return ""
    
    # Métodos para mostrar bloques de color
    def muestra_color_primario(self, obj):
        return format_html(
            '<div style="background:{}; width:50px; height:20px; border:1px solid #000"></div>',
            obj.color_primario
        )
    
    def muestra_color_secundario(self, obj):
        return format_html(
            '<div style="background:{}; width:50px; height:20px; border:1px solid #000"></div>',
            obj.color_secundario
        )
    
    def muestra_color_terciario(self, obj):
        return format_html(
            '<div style="background:{}; width:50px; height:20px; border:1px solid #000"></div>',
            obj.color_terciario
        )
    
    # Configuración adicional
    list_display_links = None  # Desactiva los enlaces
    muestra_color_primario.short_description = "Color Primario"
    muestra_color_secundario.short_description = "Color Secundario"
    muestra_color_terciario.short_description = "Color Terciario"




@admin.register(GobiernoActual)
class GobiernoActualAdmin(admin.ModelAdmin):
    list_display = ('nombre_alcalde', 'periodo', 'fecha_inicio', 'fecha_fin', 'estado_actual', 'fecha_registro')
    search_fields = ('nombre_alcalde', 'periodo')
    list_filter = ('fecha_inicio', 'fecha_fin')
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ('fecha_registro',)  # <--- Campo de solo lectura
    fieldsets = (
        ('Información de Gestión', {
            'fields': ('nombre_alcalde', 'periodo')
        }),
        ('Periodo Oficial', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        # Elimina la sección de 'Registro' del fieldsets
    )

    def estado_actual(self, obj):
        from django.utils.timezone import now
        return "En funciones" if obj.fecha_inicio <= now().date() <= obj.fecha_fin else "Finalizado"
    estado_actual.short_description = 'Estado'  # <--- Quita la coma al final

@admin.register(MisionVision)
class MisionVisionAdmin(admin.ModelAdmin):
    list_display = ('short_mision', 'short_vision', 'fecha_actualizacion')
    search_fields = ('mision', 'vision', 'valores')
    readonly_fields = ('fecha_actualizacion',)
    fieldsets = (
        ('Declaraciones Institucionales', {
            'fields': ('mision', 'vision'),
            'description': "Redacte de forma clara y concisa"
        }),
        ('Valores Corporativos', {
            'fields': ('valores',),
            'classes': ('collapse',)
        }),
        ('Control de Cambios', {
            'fields': ('fecha_actualizacion',),
            'classes': ('collapse',)
        })
    )

    def short_mision(self, obj):
        return f"{obj.mision[:70]}..." if len(obj.mision) > 70 else obj.mision
    short_mision.short_description = 'Misión (resumen)'

    def short_vision(self, obj):
        return f"{obj.vision[:70]}..." if len(obj.vision) > 70 else obj.vision
    short_vision.short_description = 'Visión (resumen)'