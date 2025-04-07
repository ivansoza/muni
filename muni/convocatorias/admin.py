from django.contrib import admin
from .models import Categoria, Convocatoria, ArchivoConvocatoria
# Register your models here.

admin.site.register(Categoria)
admin.site.register(Convocatoria)


admin.site.register(ArchivoConvocatoria)