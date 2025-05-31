# archivo: admin.py
from django.contrib import admin
from .models import Contacto

from django.utils.html import format_html


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height: 120px; border-radius: 6px;" />', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"

    list_display = (
        "municipio",
        "imagen_preview",  # miniatura en listado
        "telefono_directo",
        "correo_electronico",
        "status",
        "ultima_actualizacion",
    )

    search_fields = (
        "municipio__nombre",
        "telefono_directo",
        "correo_electronico",
        "direccion_oficinas",
    )

    list_filter = ("status", "municipio")
    ordering = ("-ultima_actualizacion",)

    readonly_fields = ("ultima_actualizacion", "imagen_preview")
    autocomplete_fields = ("municipio",)
    list_editable = ("status",)

    fieldsets = (
        (None, {
            "fields": (
                "municipio",
                "status",
                "imagen",
                "imagen_preview",
            )
        }),
        ("Información de Contacto", {
            "fields": (
                "telefono_directo",
                "correo_electronico",
                "direccion_oficinas",
            )
        }),
        ("Ubicación", {
            "fields": (
                "enlace_mapa",
                "ubicacion",
                "latitud",
                "longitud",
            )
        }),
        ("Horario de Servicio", {
            "fields": (
                "horario_servicio",
            )
        }),
        ("Redes Sociales", {
            "fields": (
                "facebook",
                "instagram",
                "youtube",
                "tiktok",
            )
        }),
        ("Números de Emergencia", {
            "fields": (
                "telefono_emergencia",
                "telefono_denuncia_anonima",
            )
        }),
        ("Control de Actualización", {
            "fields": (
                "ultima_actualizacion",
            )
        }),
    )