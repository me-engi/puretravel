# favourite/serializers.py

from rest_framework import serializers
from .models import FavoriteTour

class FavoriteTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteTour
        fields = '__all__'
