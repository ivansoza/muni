# archivo: admin.py
from django.contrib import admin
from .models import Contacto

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Contacto
    """

    list_display = (
        "municipio",
        "telefono_directo",
        "correo_electronico",
        "status",
        "ultima_actualizacion",
    )

    search_fields = (
        "municipio__nombre",  # Permite buscar por el nombre del municipio
        "telefono_directo",
        "correo_electronico",
        "direccion_oficinas",
    )

    list_filter = (
        "status",
        "municipio",
    )

    ordering = ("-ultima_actualizacion",)  # Orden por última actualización

    readonly_fields = (
        "ultima_actualizacion",
    )

    autocomplete_fields = ("municipio",)  # Para mejorar la búsqueda del municipio

    list_editable = ("status",)  # Permite editar directamente en la lista de registros

    fieldsets = (
        (None, {
            "fields": (
                "municipio",
                "status",
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
