from django.contrib import admin
from .models import MiembroGabinete, Dependencia, MiembroGabineteDirectores, MiembroGabineteRegidores, MiembroGabineteCoordinadoresDif, MiembroGabinetePresidentesComu

class MiembroGabineteInline(admin.TabularInline):
    model = MiembroGabinete
    extra = 1
    fields = ('orden', 'nombre', 'cargo', 'status', 'telefono', 'horario', 'formacion_academica', 'experiencia', 'area', 'descripcion_area', 'dependencia')
    readonly_fields = ('orden',)
    ordering = ('orden',)

@admin.register(MiembroGabinete)
class MiembroGabineteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'municipio', 'orden', 'status', 'telefono', 'horario', 'formacion_academica', 'experiencia', 'area', 'descripcion_area', 'dependencia')
    list_filter = ('municipio', 'status', 'dependencia')
    ordering = ('orden',)
    search_fields = ('nombre', 'cargo', 'telefono', 'horario', 'dependencia__nombre')
    fieldsets = (
        (None, {
            'fields': ('nombre', 'cargo', 'municipio', 'orden', 'status', 'telefono', 'horario', 'formacion_academica', 'experiencia', 'area', 'descripcion_area', 'dependencia')
        }),
        ('Fotografía', {
            'fields': ('imagen',)
        }),
        ('Contacto', {
            'fields': ('numero_contacto', 'correo_electronico', 'pagina_web')
        }),
        ('Semblanza', {
            'fields': ('semblanza',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('nombre', 'cargo', 'municipio', 'orden', 'status', 'telefono', 'horario', 'formacion_academica', 'experiencia', 'area', 'descripcion_area', 'dependencia')
        }),
    )



admin.site.register(MiembroGabineteDirectores)

admin.site.register(MiembroGabineteRegidores)

admin.site.register(MiembroGabineteCoordinadoresDif)
admin.site.register(MiembroGabinetePresidentesComu)
