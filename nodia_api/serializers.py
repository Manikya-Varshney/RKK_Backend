from rest_framework import serializers
from django.core.validators import RegexValidator
import re

class OTPSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex = r'^\+\d{4,15}$', message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = serializers.CharField(max_length = 17, validators = [phone_regex])