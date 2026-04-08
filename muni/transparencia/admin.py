from django.contrib import admin
from .models import Encuesta, Pregunta, Opcion, Envio, Respuesta
from .models import ListaObligaciones, ArticuloLiga,LigaArchivo

# Inline para editar Opciones dentro de una Pregunta
class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 1  # Número de formularios adicionales que se muestran por defecto

# Inline para editar Preguntas dentro de una Encuesta
class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1

# Configuración del admin para Encuesta, incluyendo sus preguntas en línea
@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    inlines = [PreguntaInline]

# Configuración del admin para Pregunta, incluyendo las opciones en línea
@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'encuesta', 'orden')
    list_filter = ('encuesta',)
    ordering = ('encuesta', 'orden')
    inlines = [OpcionInline]

# Configuración básica para Opcion
@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ('texto', 'pregunta')
    list_filter = ('pregunta',)

# Inline para editar Respuestas dentro de un Envio
class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 0

# Configuración del admin para Envio, mostrando las respuestas asociadas
@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ('id', 'encuesta', 'fecha_envio')
    list_filter = ('encuesta', 'fecha_envio')
    inlines = [RespuestaInline]

# Configuración básica para Respuesta
@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('envio', 'pregunta', 'opcion')
    list_filter = ('pregunta', 'opcion', 'envio')
from .models import SeccionTransparencia, EjercicioFiscal, DocumentoTransparencia
# Register your models here.

admin.site.register(SeccionTransparencia)
admin.site.register(EjercicioFiscal)
admin.site.register(DocumentoTransparencia)
admin.site.register(ListaObligaciones)
admin.site.register(ArticuloLiga)
admin.site.register(LigaArchivo)