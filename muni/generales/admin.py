# admin.py
from django.contrib import admin
from .models import SocialNetwork

@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = (
        'municipio',
        'social_type',
        'social_username',
        'is_favorite',
        'fecha_creacion',
        'fecha_actualizacion',
    )
    list_filter = ('municipio', 'social_type', 'is_favorite')
    search_fields = ('social_username', 'social_url', 'municipio__nombre_municipio')
    ordering = ('municipio', 'social_type')