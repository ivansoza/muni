from django.contrib import admin

from privacidad.models import ArchivoRelacionado, AvisoDePrivacidad


# Administrador para Aviso de Privacidad
class AvisoDePrivacidadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'municipio', 'fecha_creacion')
    search_fields = ('titulo', 'municipio__nombre')  # Permite buscar por título y municipio
    list_filter = ('municipio',)  # Filtro por municipio
    ordering = ('-fecha_creacion',)  # Ordena por fecha de creación (más reciente primero)

# Administrador para Archivos Relacionados
class ArchivoRelacionadoAdmin(admin.ModelAdmin):
    list_display = ('aviso_privacidad', 'descripcion', 'archivo', 'fecha_subida')
    search_fields = ('aviso_privacidad__titulo', 'descripcion')  # Permite buscar por título del aviso y descripción
    list_filter = ('aviso_privacidad',)  # Filtro por aviso de privacidad
    ordering = ('-fecha_subida',)  # Ordena por fecha de subida (más reciente primero)

# Registrar los modelos en el admin
admin.site.register(AvisoDePrivacidad, AvisoDePrivacidadAdmin)
admin.site.register(ArchivoRelacionado, ArchivoRelacionadoAdmin)