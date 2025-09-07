from rest_framework import serializers
from .models import GenelAyar

class GenelAyarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenelAyar
        fields = ['id', 'isletme_adi', 'aciklama', 'logo', 'acilis_saati', 'kapanis_saati', 'slug'] 