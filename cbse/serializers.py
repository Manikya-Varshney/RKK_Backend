from rest_framework import serializers

from .models import *


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class StandardSerializer(serializers.ModelSerializer):
    boards = BoardSerializer(many = True)

    class Meta:
        model = Standard
        fields = ['name','id','is_locked','boards']