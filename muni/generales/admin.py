# admin.py
from django.contrib import admin
from .models import AppIcon, ArchivoRelacionadoRecomendacion, ContadorVisitas, MetaMunicipio, Recomendaciones, SeccionPlus, Secciones, SocialNetwork, personalizacionPlantilla, VideoMunicipio, SeccionPlusArchivo
from django.utils.html import format_html

@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = (
        'municipio',
        'social_type',
        'social_username',
        'is_favorite',
        'fecha_creacion',
        'fecha_actualizacion',
    )
    list_filter = ('municipio', 'social_type', 'is_favorite')
    search_fields = ('social_username', 'social_url', 'municipio__nombre_municipio')
    ordering = ('municipio', 'social_type')

admin.site.register(ContadorVisitas)
admin.site.register(Secciones)

@admin.register(personalizacionPlantilla)
class PersonalizacionPlantillaAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'entrada','hero_seccion')
    list_filter = ('entrada','hero_seccion')
    search_fields = ('municipio__nombre',)


class MetaMunicipioAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'meta_title', 'meta_description')
    search_fields = ('municipio__nombre', 'meta_title')

admin.site.register(MetaMunicipio, MetaMunicipioAdmin)


admin.site.register(SeccionPlus)


class ArchivoRelacionadoRecomendacionInline(admin.TabularInline):
    model = ArchivoRelacionadoRecomendacion
    extra = 1
    readonly_fields = ('fecha_subida',)
    fields = ('archivo', 'descripcion', 'fecha_subida')

@admin.register(Recomendaciones)
class RecomendacionesAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'area', 'fecha_creacion')
    list_filter = ('municipio',)
    search_fields = ('area', 'descripcion')
    readonly_fields = ('fecha_creacion',)
    date_hierarchy = 'fecha_creacion'
    inlines = (ArchivoRelacionadoRecomendacionInline,)

@admin.register(ArchivoRelacionadoRecomendacion)
class ArchivoRelacionadoRecomendacionAdmin(admin.ModelAdmin):
    list_display = ('recomendacion', 'descripcion', 'fecha_subida')
    search_fields = ('descripcion',)
    readonly_fields = ('fecha_subida',)




admin.site.register(VideoMunicipio)
admin.site.register(SeccionPlusArchivo)



@admin.register(AppIcon)
class AppIconAdmin(admin.ModelAdmin):
    list_display = ('get_app_display_name', 'imagen_preview', 'imagen')
    list_editable = ('imagen',)

    def get_app_display_name(self, obj):
        return obj.get_app_display()
    get_app_display_name.short_description = 'Aplicación'

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width:50px; height:50px; border-radius:10px; object-fit:cover;">', obj.imagen.url)
        return '—'
    imagen_preview.short_description = 'Vista previa'