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
            # board_data = validated_data.pop('board', None)
            print(validated_data.get('board'), validated_data.get('id'))
            id = validated_data.get('id')
            board = Board.objects.get(id = id)
            instance.board = board

        if 'language' in validated_data:
            # language_data = validated_data.pop('language', None)
            # language = Language.objects.get(**language_data)
            instance.language = validated_data.get('language')

        if 'standard' in validated_data:
            instance.standard = validated_data.get('standard')

        # if 'subjects' in validated_data:
        #     instance.subjects.clear()
        #     for s in validated_data.get('subjects'):
        #         # subject = Subject.objects.get(id = s)
        #         instance.subjects.add(s)

        instance.save()
        return instance
