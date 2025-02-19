# admin.py
from django.contrib import admin
from .models import  MiembroGabinete

class MiembroGabineteInline(admin.TabularInline):
    model = MiembroGabinete
    extra = 1
    fields = ('orden', 'nombre', 'cargo', 'status')
    readonly_fields = ()
    ordering = ('orden',)


@admin.register(MiembroGabinete)
class MiembroGabineteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'municipio', 'orden', 'status')
    list_filter = ('municipio', 'status')
    ordering = ('orden',)
    search_fields = ('nombre', 'cargo')
