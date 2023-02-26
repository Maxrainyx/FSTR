from .models import (
    User, Coordinates, Level, Images, Pass
)
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class PassSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    coordinates = CoordinatesSerializer(read_only=True)
    levels = LevelSerializer(read_only=True)
    images = ImagesSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Pass
        fields = '__all__'
