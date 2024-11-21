# Generated by Django 5.1.1 on 2024-11-21 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ajustes', '0005_rename_archivos_archivo_alter_archivo_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='tipo_de_archivo',
            field=models.CharField(choices=[('imagen', 'Imagen'), ('wysiwyg', 'Wysiwyg'), ('audio', 'Audio'), ('video', 'Video'), ('subtitulo', 'Subtítulo'), ('manual', 'Manual')], max_length=50),
        ),
    ]