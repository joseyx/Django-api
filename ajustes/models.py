from django.core.exceptions import ValidationError
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

class Archivo(models.Model):
    TIPO_DE_ARCHIVO_CHOICES = [
        ('imagen', 'Imagen'),
        ('wysiwyg', 'Wysiwyg'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('subtitulo', 'Subtítulo'),
        ('manual', 'Manual'),
    ]

    tipo_de_archivo = models.CharField(max_length=50, choices=TIPO_DE_ARCHIVO_CHOICES)
    archivo = models.FileField(upload_to='archivos/')

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

    def __str__(self):
        return f"Archivo: {self.archivo}"

    def save(self, *args, **kwargs):
        if self.tipo_de_archivo == 'wysiwyg' and Archivo.objects.filter(tipo_de_archivo='wysiwyg').count() >= 1:
            raise ValidationError("Solo se permite 1 archivo Wysiwyg.")
        if self.tipo_de_archivo == 'audio' and Archivo.objects.filter(tipo_de_archivo='audio').count() >= 3:
            raise ValidationError("Solo se permiten 3 archivos de audio.")
        if self.tipo_de_archivo == 'video' and Archivo.objects.filter(tipo_de_archivo='video').count() >= 1:
            raise ValidationError("Solo se permite 1 archivo de video.")
        if self.tipo_de_archivo == 'subtitulo' and Archivo.objects.filter(tipo_de_archivo='subtitulo').count() >= 5:
            raise ValidationError("Solo se permiten 5 archivos de subtítulo.")
        if self.tipo_de_archivo == 'manual' and Archivo.objects.filter(tipo_de_archivo='manual').count() >= 1:
            raise ValidationError("Solo se permite 1 archivo manual.")
        super().save(*args, **kwargs)