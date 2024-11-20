from rest_framework import serializers

from .models import Ajustes, Archivo

class AjustesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ajustes
        fields = [
            'font_size_title',
            'font_size_subtitle',
            'font_size_paragraph',
            'color_primary',
            'color_secondary',
            'color_tertiary',
            'font_file'
        ]

class AjustesUpdateSerializer(serializers.ModelSerializer):
    font_file = serializers.FileField(required=False)

    class Meta:
        model = Ajustes
        fields = [
            'font_size_title',
            'font_size_subtitle',
            'font_size_paragraph',
            'color_primary',
            'color_secondary',
            'color_tertiary',
            'font_file'
        ]

    def update(self, instance, validated_data):
        print('File:', validated_data.get('font_file', None))
        # Check if font_file is present and is a valid file
        font_file = validated_data.get('font_file', None)
        if font_file and not hasattr(font_file, 'read'):
            validated_data.pop('font_file')

        return super().update(instance, validated_data)

class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = '__all__'
