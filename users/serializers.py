from rest_framework import fields, serializers

from cbse.models import Board, Language, Standard, Subject
from .models import Profile
from cbse.serializers import BoardSerializer, LanguageSerializer, StandardSerializer, SubjectSerializer

class ProfileSerializer(serializers.ModelSerializer):

    # subjects = serializers.PrimaryKeyRelatedField(many = True,  read_only = True)
    # language = serializers.PrimaryKeyRelatedField(many = False, read_only = True)
    # standard = serializers.PrimaryKeyRelatedField(many = False, read_only = True)
    # board = serializers.PrimaryKeyRelatedField(many = False, read_only = True)
    language = LanguageSerializer(many = False)
    standard = StandardSerializer(many = False)
    board = BoardSerializer(many = False)
    subjects = SubjectSerializer(many = True, required = False)

    class Meta:
        model = Profile
        fields = ['phone_number', 'name', 'otp', 'otp_timestamp', 'city', 'state', 'board', 'language', 'standard','subjects']
        extra_kwargs = {'subjects': {'required': False}}
        depth = 1

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data)

        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        if 'board' in validated_data:
            id = validated_data['board']['id']
            board = Board.objects.get(id = id)
            instance.board = board

        if 'language' in validated_data:
            id = validated_data['language']['id']
            language = Language.objects.get(id = id)
            # language_data = validated_data.pop('language', None)
            # language = Language.objects.get(**language_data)
            instance.language = language

        if 'standard' in validated_data:
            id = validated_data['standard']['id']
            standard = Standard.objects.get(id = id)
            instance.standard = standard

        if 'subjects' in validated_data:
            instance.subjects.clear()
            for s in validated_data.get('subjects'):
                subject = Subject.objects.get(id = s['id'])
                instance.subjects.add(subject)

        instance.save()
        return instance
