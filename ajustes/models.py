import os
import subprocess

from PIL import Image
from django.core.exceptions import ValidationError
from django.db import models
import mutagen
import imghdr

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

    name = models.CharField(max_length=255, null=True, blank=True)  # New name field
    tipo_de_archivo = models.CharField(max_length=50, choices=TIPO_DE_ARCHIVO_CHOICES)
    archivo = models.FileField(upload_to='archivos/')
    peso = models.PositiveIntegerField(null=True, blank=True)  # Peso del archivo en bytes
    ancho = models.PositiveIntegerField(null=True, blank=True)  # Ancho de la imagen
    alto = models.PositiveIntegerField(null=True, blank=True)  # Alto de la imagen
    duracion = models.PositiveIntegerField(null=True, blank=True)  # Duración en segundos
    formato = models.CharField(max_length=50, null=True, blank=True)  # Formato del archivo

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

    def __str__(self):
        return f"Archivo: {self.archivo}"

    def save(self, *args, **kwargs):
        try:
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

            # Set the name field to the file name
            self.name = os.path.basename(self.archivo.name)

            # Save the file first to ensure it exists on the filesystem
            super().save(*args, **kwargs)

            # Set file size in KB
            self.peso = self.archivo.size / 1024
            file_path = self.archivo.path

            # Verify and set image dimensions
            if self.tipo_de_archivo == 'imagen':
                if imghdr.what(file_path) is None:
                    raise ValidationError("El archivo no es una imagen válida.")
                image = Image.open(self.archivo)
                self.ancho, self.alto = image.size
                self.formato = image.format.lower()

                # Resize the image to 1920x1080
                image = image.resize((1920, 1080))
                image.save(self.archivo.path)

            # Verify and set duration and format for audio
            if self.tipo_de_archivo == 'audio':
                media_info = mutagen.File(file_path)
                if media_info is None or not media_info.mime[0].startswith('audio'):
                    raise ValidationError("El archivo no es un audio válido.")
                self.duracion = int(media_info.info.length)
                self.formato = media_info.mime[0]

            # Verify video file extension and set duration
            if self.tipo_de_archivo == 'video':
                valid_video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
                ext = os.path.splitext(file_path)[1].lower()
                if ext not in valid_video_extensions:
                    raise ValidationError("El archivo no tiene una extensión de video válida.")
                self.formato = ext[1:]  # Set the format to the file extension without the dot

                # Get video duration using ffprobe
                try:
                    result = subprocess.run(
                        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
                        capture_output=True, text=True, check=True
                    )
                    self.duracion = int(float(result.stdout.strip()))
                except subprocess.CalledProcessError:
                    raise ValidationError("No se pudo obtener la duración del video.")

            # Verify subtitle file extension
            if self.tipo_de_archivo == 'subtitulo':
                valid_subtitle_extensions = ['.srt', '.vtt', '.ass', '.ssa']
                ext = os.path.splitext(file_path)[1].lower()
                if ext not in valid_subtitle_extensions:
                    raise ValidationError("El archivo no tiene una extensión de subtítulo válida.")
                self.formato = ext[1:]  # Set the format to the file extension without the dot

            # Verify manual file extension
            if self.tipo_de_archivo == 'manual':
                valid_manual_extensions = ['.pdf', '.doc', '.docx']
                ext = os.path.splitext(file_path)[1].lower()
                if ext not in valid_manual_extensions:
                    raise ValidationError("El archivo no tiene una extensión de manual válida.")
                self.formato = ext[1:]  # Set the format to the file extension without the dot

            # Save again to update the fields
            super().save(update_fields=['peso', 'ancho', 'alto', 'duracion', 'formato'])

        except ValidationError as e:
            # Delete the file if an error is detected
            self.archivo.delete(save=False)
            raise e

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        self.archivo.delete(save=False)
        # Call the superclass delete method
        super().delete(*args, **kwargs)