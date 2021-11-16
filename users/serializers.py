from rest_framework import fields, serializers

from cbse.models import Board, Language, Standard
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = ['phone_number', 'name', 'otp', 'otp_timestamp', 'city', 'state', 'board', 'language', 'standard']
        extra_kwargs = {'phone_number': {'required': False}, 'subjects': {'required': False}, 'board':{'read_only':True}}

        def update(self, instance, data):
            instance.name = self.data.get('name', instance.name)
            instance.phone_number = self.data.get('phone_number', instance.phone_number)
            instance.city = self.data.get('city', instance.city)
            instance.state = self.data.get('state', instance.state)
            print(self.data)
            if 'board' in self.data:
                board = Board.objects.get(id = self.data.get('board'))
                instance.board = board

            if 'language' in self.data:
                language = Language.objects.get(id = self.data.get('language'))
                instance.board = language

            if 'standard' in self.data:
                standard = Standard.objects.get(id = self.data.get('standard'))
                instance.board = standard

            if 'subjects' in self.data:
                for s in self.data.get('subjects'):
                    subject = Subject.objects.get(id = s)
                    instance.subjects.add(subject)

            instance.save()
            return instance
