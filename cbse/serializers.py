from django.db.models import fields
from rest_framework import serializers
from users.models import Plan

from .models import *


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Board
        fields = ['name','id']

class StandardSerializer(serializers.ModelSerializer):
    board = BoardSerializer(many = False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Standard
        fields = ['name','id','is_locked','board']

class SubjectSerializer(serializers.ModelSerializer):
    standard = StandardSerializer(many = False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Subject
        fields = ['id','name','standard']

class ChapterSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many = False)
    pdf_count = serializers.SerializerMethodField('get_pdf_count')

    def get_pdf_count(self, chapter_document):
        return chapter_document.documents.count()


    class Meta:
        model = Chapter
        fields = ['name','subject','id','is_locked','pdf_count']

class LanguageSerializer(serializers.ModelSerializer):
    board = BoardSerializer(many = False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Language
        fields = ['name','id','board']
        # depth = 1

class ChapterDocumentsSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer(many = False)

    class Meta:
        model = ChapterDocument
        fields = ['name','chapter','pdf_link','is_locked','rank']
