from django import template

register = template.Library()

@register.filter
def filter_nav(secciones, nav_seccion):
    return [s for s in secciones if s.nav_seccion == nav_seccion and s.status]