# reportes/models.py
from __future__ import annotations

import secrets
import string

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from informacion_municipal.models import Municipio

# ───────────────────────────────────────── helper ──────────────────────────────────────────
_ALFABETO = string.ascii_uppercase + string.digits


def _codigo_unico(modelo: type[models.Model], longitud: int = 8) -> str:
    """
    Genera un código alfanumérico corto y garantiza que sea único en la tabla indicada.
    """
    while True:
        codigo = "".join(secrets.choice(_ALFABETO) for _ in range(longitud))
        if not modelo.objects.filter(codigo_seguimiento=codigo).exists():
            return codigo


# ───────────────────────────── clase base (NO crea tabla) ────────────────────────────────
class ReporteBase(models.Model):
    """
    Campos comunes a cualquier tipo de reporte municipal.
    """

    codigo_seguimiento = models.CharField(
        _("código de seguimiento"),
        max_length=10,
        unique=True,
        editable=False,
        help_text=_("Se genera automáticamente; compártelo con la ciudadanía."),
    )
    nombre_solicitante = models.CharField(
        _("nombre de quien reporta"), max_length=120
    )
    descripcion = models.TextField(_("descripción / comentarios"))
    foto = models.ImageField(
        _("fotografía (opcional)"),
        upload_to="reportes/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    ubicacion = models.CharField(
        _("ubicación (texto libre)"),
        max_length=255,
        help_text=_("Ej. Calle, número, colonia, referencia visual…"),
    )
    latitud = models.DecimalField(
        _("latitud"), max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitud = models.DecimalField(
        _("longitud"), max_digits=9, decimal_places=6, blank=True, null=True
    )


    place_id = models.CharField(
        _("Google Place ID"), max_length=255,
        blank=True, null=True, db_index=True
    )
    class Estatus(models.TextChoices):
        PENDIENTE = "PEND", _("Pendiente")
        EN_PROGRESO = "ENPR", _("En progreso")
        RESUELTO = "RES", _("Resuelto")
        CERRADO = "CER", _("Cerrado / sin acción")

    estatus = models.CharField(
        _("estatus"),
        max_length=4,
        choices=Estatus.choices,
        default=Estatus.PENDIENTE,
    )
    creado = models.DateTimeField(_("creado"), auto_now_add=True)
    actualizado = models.DateTimeField(_("actualizado"), auto_now=True)

    class Meta:
        abstract = True  # Garantiza que no se cree tabla para ReporteBase
        ordering = ("-creado",)

    # Representación legible
    def __str__(self) -> str:  # pragma: no cover
        return f"{self._meta.verbose_name.title()} #{self.codigo_seguimiento}"

    # Sobrecarga del save para asignar código único •una sola vez•
    def save(self, *args, **kwargs):  # noqa: D401
        if not self.codigo_seguimiento:
            self.codigo_seguimiento = _codigo_unico(self.__class__)
        super().save(*args, **kwargs)


# ───────────────────────────────── modelos específicos ────────────────────────────────────
class ReporteServicioAgua(ReporteBase):
    class Meta(ReporteBase.Meta):
        verbose_name = _("reporte de servicio de agua")
        verbose_name_plural = _("reportes de servicio de agua")


class ReporteBache(ReporteBase):
    class Meta(ReporteBase.Meta):
        verbose_name = _("reporte de bache")
        verbose_name_plural = _("reportes de bache")


class ReporteAlcantarillado(ReporteBase):
    class Meta(ReporteBase.Meta):
        verbose_name = _("reporte de alcantarillado")
        verbose_name_plural = _("reportes de alcantarillado")


class ReporteAlumbradoPublico(ReporteBase):
    class Meta(ReporteBase.Meta):
        verbose_name = _("reporte de alumbrado público")
        verbose_name_plural = _("reportes de alumbrado público")



class ReporteStatus(models.Model):
    """Debe existir **solo un** registro en toda la tabla."""

    reporte_agua_status = models.BooleanField(
        _("reporte de agua habilitado"), default=False
    )
    reporte_bache_status = models.BooleanField(
        _("reporte de bache habilitado"), default=False
    )
    reporte_alcantarillado_status = models.BooleanField(
        _("reporte de alcantarillado habilitado"), default=False
    )
    reporte_alumbrado_status = models.BooleanField(
        _("reporte de alumbrado público habilitado"), default=False
    )

    class Meta:
        verbose_name = _("estatus de reportes")
        verbose_name_plural = _("estatus de reportes")

    def __str__(self):
        return "Estatus de reportes"

    # ───────── clave: impedir más de un registro ─────────
    def save(self, *args, **kwargs):
        if not self.pk and ReporteStatus.objects.exists():
            raise ValidationError(
                _("Solo puede existir un objeto de ReporteStatus.")
            )
        super().save(*args, **kwargs)