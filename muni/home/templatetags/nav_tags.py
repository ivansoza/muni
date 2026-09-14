"""Filtros para agrupar las secciones activas del menú municipal."""

from django import template

register = template.Library()


@register.filter
def filter_nav(secciones, nav_seccion):
    """Conserva el orden y muestra las secciones activas del grupo indicado."""
    if secciones is None:
        return []
    return [
        seccion
        for seccion in secciones
        if seccion.status and seccion.nav_seccion == nav_seccion
    ]
