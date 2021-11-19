from django.db.models import fields
from rest_framework import serializers
from users.models import Plan

from .models import *


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['name','id']

class StandardSerializer(serializers.ModelSerializer):
    board = BoardSerializer(many = False)

    class Meta:
        model = Standard
        fields = ['name','id','is_locked','board']

class SubjectSerializer(serializers.ModelSerializer):
    standard = StandardSerializer(many = False)
    class Meta:
        model = Subject
        fields = ['id','name','standard']

class ChapterSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many = False)

    class Meta:
        model = Chapter
        fields = ['name','chapter_link','subject','id','is_locked']

class LanguageSerializer(serializers.ModelSerializer):
    # board = BoardSerializer(many = False)
    board = serializers.PrimaryKeyRelatedField(many = False, read_only = True)
    class Meta:
        model = Language
        fields = ['name','id','board']