from django.contrib import admin
from django.utils.html import format_html
from .models import ElementoLista, InformacionCiudad, Municipio, ColoresMunicipio, GobiernoActual, MisionVision,SeccionInicio, Video

# Registro de Municipio
@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ultima_actualizacion', 'preview_logotipo', 'preview_logotipo_claro', 'preview_banner', 'status')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('ultima_actualizacion',)
    readonly_fields = ('preview_logotipo', 'preview_logotipo_claro', 'preview_banner', 'ultima_actualizacion')

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_municipio', 'nombre', 'descripcion', 'status')
        }),
        ('Elementos Visuales', {
            'fields': (
                ('logotipo', 'preview_logotipo'),
                ('logotipo_claro', 'preview_logotipo_claro'),
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

    # Vista previa del logotipo principal
    def preview_logotipo(self, obj):
        if obj.logotipo:
            return format_html(
                '<div style="border: 1px solid #ddd; padding: 5px; display: inline-block">'
                '<img src="{}" style="max-height: 60px; max-width: 120px; object-fit: contain"/>'
                '</div>',
                obj.logotipo.url
            )
        return "-"
    preview_logotipo.short_description = 'Logo Principal'

    # Vista previa del logotipo para fondos claros
    def preview_logotipo_claro(self, obj):
        if obj.logotipo_claro:
            return format_html(
                '<div style="border: 1px solid #ddd; padding: 5px; display: inline-block; background: #f5f5f5">'
                '<img src="{}" style="max-height: 60px; max-width: 120px; object-fit: contain"/>'
                '</div>',
                obj.logotipo_claro.url
            )
        return "-"
    preview_logotipo_claro.short_description = 'Logo Fondos Claros'

    # Vista previa del banner
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


@admin.register(ColoresMunicipio)
class ColoresMunicipioAdmin(admin.ModelAdmin):
    list_editable = ("color_primario", "color_secundario")
    list_display = (
        "municipio",
        "muestra_color_primario", "color_primario",
        "muestra_color_primario_dark", "color_primario_dark",
        "muestra_color_primario_light", "color_primario_light",
        "muestra_color_primario_rgb", "color_primario_rgb",
        "muestra_color_primario_dark_rgb", "color_primario_dark_rgb",
        "muestra_color_secundario", "color_secundario",
        "muestra_color_secundario_dark", "color_secundario_dark",
        "muestra_color_secundario_light", "color_secundario_light",
        "muestra_color_secundario_rgb", "color_secundario_rgb",
        "muestra_color_secundario_dark_rgb", "color_secundario_dark_rgb",
        "fecha_creacion",
    )

    # Bloque visual para el color primario en HEX
    def muestra_color_primario(self, obj):
        return format_html('<div style="background:{}; width:50px; height:20px; border:1px solid #000;"></div>', obj.color_primario)
    muestra_color_primario.short_description = "Color Primario"
    
    # Bloque visual para el color primario dark en HEX
    def muestra_color_primario_dark(self, obj):
        return format_html('<div style="background:{}; width:50px; height:20px; border:1px solid #000;"></div>', obj.color_primario_dark)
    muestra_color_primario_dark.short_description = "Primario Dark"
    
    # Bloque visual para el color primario light en HEX
    def muestra_color_primario_light(self, obj):
        return format_html('<div style="background:{}; width:50px; height:20px; border:1px solid #000;"></div>', obj.color_primario_light)
    muestra_color_primario_light.short_description = "Primario Light"
    
    # Mostrar el RGB (números) para el color primario
    def muestra_color_primario_rgb(self, obj):
        return obj.color_primario_rgb
    muestra_color_primario_rgb.short_description = "Primario RGB"
    
    # Mostrar el RGB (números) para el color primario dark
    def muestra_color_primario_dark_rgb(self, obj):
        return obj.color_primario_dark_rgb
    muestra_color_primario_dark_rgb.short_description = "Primario Dark RGB"
    
    # Bloque visual para el color secundario en HEX
    def muestra_color_secundario(self, obj):
        return format_html('<div style="background:{}; width:50px; height:20px; border:1px solid #000;"></div>', obj.color_secundario)
    muestra_color_secundario.short_description = "Color Secundario"
    
    # Bloque visual para el color secundario dark en HEX
    def muestra_color_secundario_dark(self, obj):
        return format_html('<div style="background:{}; width:50px; height:20px; border:1px solid #000;"></div>', obj.color_secundario_dark)
    muestra_color_secundario_dark.short_description = "Secundario Dark"
    
    # Bloque visual para el color secundario light en HEX
    def muestra_color_secundario_light(self, obj):
        return format_html('<div style="background:{}; width:50px; height:20px; border:1px solid #000;"></div>', obj.color_secundario_light)
    muestra_color_secundario_light.short_description = "Secundario Light"
    
    # Mostrar el RGB (números) para el color secundario
    def muestra_color_secundario_rgb(self, obj):
        return obj.color_secundario_rgb
    muestra_color_secundario_rgb.short_description = "Secundario RGB"
    
    # Mostrar el RGB (números) para el color secundario dark
    def muestra_color_secundario_dark_rgb(self, obj):
        return obj.color_secundario_dark_rgb
    muestra_color_secundario_dark_rgb.short_description = "Secundario Dark RGB"
    
    list_display_links = ("municipio",)
@admin.register(GobiernoActual)
class GobiernoActualAdmin(admin.ModelAdmin):
    list_display = ('nombre_alcalde', 'periodo', 'fecha_inicio', 'fecha_fin', 'estado_actual', 'fecha_registro')
    search_fields = ('nombre_alcalde', 'periodo')
    list_filter = ('fecha_inicio', 'fecha_fin')
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ('fecha_registro',)  # Campo de solo lectura

    fieldsets = (
        ('Información de Gestión', {
            'fields': ('nombre_alcalde', 'periodo')
        }),
        ('Periodo Oficial', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
    )

    def estado_actual(self, obj):
        from django.utils.timezone import now
        return "En funciones" if obj.fecha_inicio <= now().date() <= obj.fecha_fin else "Finalizado"
    estado_actual.short_description = 'Estado'

# Registro de MisionVision
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


admin.site.register(SeccionInicio)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'municipio', 'url_video', 'canal_youtube')
    search_fields = ('titulo',)



admin.site.register(Video, VideoAdmin)


class ElementoListaInline(admin.TabularInline):
    model = ElementoLista
    extra = 1  # Número de elementos en blanco a mostrar por defecto
    fields = ('texto',)
    verbose_name = "Elemento de la lista"
    verbose_name_plural = "Elementos de la lista"

@admin.register(InformacionCiudad)
class InformacionCiudadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'municipio', 'lema')
    search_fields = ('titulo', 'subtitulo', 'lema', 'municipio__nombre')
    list_filter = ('municipio',)
    inlines = [ElementoListaInline]
    fieldsets = (
        (None, {
            'fields': ('municipio', 'lema', 'titulo', 'subtitulo', 'encabezado_lista')
        }),
    )

@admin.register(ElementoLista)
class ElementoListaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'informacion')
    search_fields = ('texto',)
    list_filter = ('informacion',)