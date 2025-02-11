# myapp/templatetags/render_dynamic.py
from django import template
from django.template import Template, Context
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def render_dynamic(content, extra_context=None):
    """
    Toma el contenido (string) y lo compila como un template,
    usando extra_context (debe ser un diccionario) si se proporciona.
    """
    try:
        extra_context = extra_context or {}
        # Crea un template a partir del contenido
        tmpl = Template(content)
        # Renderiza el template usando un Context combinado con el contexto actual
        context = Context(extra_context)
        rendered = tmpl.render(context)
        return mark_safe(rendered)
    except Exception as e:
        # En caso de error, puedes registrar el problema o devolver el contenido original
        return content
