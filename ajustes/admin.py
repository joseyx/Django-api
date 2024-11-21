from django.contrib import admin
from .models import Ajustes, Archivo

# Register your models here.

@admin.register(Ajustes)
class AjustesAdmin(admin.ModelAdmin):
    list_display = (
        'font_size_title',
        'font_size_subtitle',
        'font_size_paragraph',
        'color_primary',
        'color_secondary',
        'color_tertiary',
        'font_file',
    )
    list_filter = (
        'font_size_title',
        'font_size_subtitle',
        'font_size_paragraph',
        'color_primary',
        'color_secondary',
        'color_tertiary',
        'font_file',
    )
    search_fields = (
        'font_size_title',
        'font_size_subtitle',
        'font_size_paragraph',
        'color_primary',
        'color_secondary',
        'color_tertiary',
        'font_file',
    )
    ordering = (
        'font_size_title',
        'font_size_subtitle',
        'font_size_paragraph',
        'color_primary',
        'color_secondary',
        'color_tertiary',
        'font_file',
    )

@admin.register(Archivo)
class ArchivosAdmin(admin.ModelAdmin):
    list_display = (
        'tipo_de_archivo',
        'archivo',
        'peso',
        'ancho',
        'alto',
        'duracion',
        'formato',
    )
    list_filter = (
        'tipo_de_archivo',
        'archivo',
    )
    search_fields = (
        'tipo_de_archivo',
        'archivo',
    )
    ordering = (
        'tipo_de_archivo',
        'archivo',
    )
    readonly_fields = (
        'peso',
        'ancho',
        'alto',
        'duracion',
        'formato',
    )

