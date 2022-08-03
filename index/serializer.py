from rest_framework import serializers
from .models import Game

class Game_serializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'year', 'description', 'studio', 'rating', 'poster', 'rubric')
        model = Game