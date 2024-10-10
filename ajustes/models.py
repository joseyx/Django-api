from django.db import models

class Ajustes(models.Model):
    # Tamaños de fuentes
    font_size_title = models.CharField(max_length=10)
    font_size_subtitle = models.CharField(max_length=10)
    font_size_paragraph = models.CharField(max_length=10)

    # Colores en formato hexadecimal
    color_primary = models.CharField(max_length=7)  # Ejemplo: '#FF5733'
    color_secondary = models.CharField(max_length=7)
    color_tertiary = models.CharField(max_length=7)

    # Fuente
    font_file = models.FileField(upload_to='fonts/', null=True, blank=True)

    def __str__(self):
        return f"Ajustes: Font Sizes - {self.font_size_title}, {self.font_size_subtitle}, {self.font_size_paragraph}"
