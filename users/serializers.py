from rest_framework import fields, serializers

from cbse.models import Board, Language, Standard, Subject
from .models import Profile
from cbse.serializers import BoardSerializer, LanguageSerializer, StandardSerializer, SubjectSerializer, PlanSerializer

from datetime import datetime

class ProfileSerializer(serializers.ModelSerializer):

    # subjects = serializers.PrimaryKeyRelatedField(many = True,  read_only = True)
    # language = serializers.PrimaryKeyRelatedField(many = False, read_only = True)
    # standard = serializers.PrimaryKeyRelatedField(many = False, read_only = True)
    # board = serializers.PrimaryKeyRelatedField(many = False, read_only = True)
    language = LanguageSerializer(many = False, required = False, allow_null = True)
    standard = StandardSerializer(many = False, required = False, allow_null = True)
    board = BoardSerializer(many = False, required = False, allow_null = True)
    subjects = SubjectSerializer(many = True, required = False)
    plan = PlanSerializer(many = False, required = False, allow_null = True)
    days_remaining = serializers.SerializerMethodField('days_remaining_method')

    def days_remaining_method(self, profile):
        days_remaining = datetime.now().date() - profile.plan_start_date.date()
        return profile.plan.number_of_days - days_remaining.days

    class Meta:
        model = Profile
        fields = ['phone_number', 'name', 'otp', 'otp_timestamp', 'city', 'state', 'board', 'language', 'standard', 'subjects', 'plan', 'days_remaining']
        extra_kwargs = {'subjects': {'required': False},'subjects': {'language': False},'standard': {'required': False}, 'subjects': {'board': False}}
        depth = 1

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):

        if 'name' in validated_data and validated_data['name']:
            instance.name = validated_data['name']

        if 'phone_number' in validated_data and validated_data['phone_number']:
            instance.phone_number = validated_data['phone_number']

        if 'city' in validated_data and validated_data['city']:
            instance.city = validated_data['city']

        if 'state' in validated_data and validated_data['state']:
            instance.state = validated_data['state']

        # instance.name = validated_data.get('name', instance.name)[validated_data.get('name', None) is None]
        # instance.phone_number = validated_data.get('phone_number', instance.phone_number)[validated_data.get('phone_number', None) is None]
        # instance.city = validated_data.get('city', instance.city)[validated_data.get('city', None) is None]
        # instance.state = validated_data.get('state', instance.state)[validated_data.get('state', None) is None]

        if 'board' in validated_data and validated_data['board']:
            id = validated_data['board']['id']
            board = Board.objects.get(id = id)
            instance.board = board

        if 'language' in validated_data and validated_data['language']:
            id = validated_data['language']['id']
            language = Language.objects.get(id = id)
            # language_data = validated_data.pop('language', None)
            # language = Language.objects.get(**language_data)
            instance.language = language

        if 'standard' in validated_data and validated_data['standard']:
            id = validated_data['standard']['id']
            standard = Standard.objects.get(id = id)
            instance.standard = standard

        if 'subjects' in validated_data:
            instance.subjects.clear()
            for s in validated_data.get('subjects'):
                print("s", s)
                subject = Subject.objects.get(id = s['id'])
                instance.subjects.add(subject)

        instance.save()
        return instance
