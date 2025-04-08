# admin.py
from django.contrib import admin
from .models import ContadorVisitas, MetaMunicipio, SeccionPlus, Secciones, SocialNetwork, personalizacionPlantilla

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
