from django.shortcuts import render

from nodia import Constants
from . import utils

from .serializers import *

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(["POST"])
def generate_otp(request):
    if request.method == "POST":
        hashValue = request.POST.get(Constants.HASH)
        phone_number = request.POST.get(Constants.PHONE_NUMBER) 

        otp = utils.otp_generator()
        serializer = OTPSerializer(data = request.data)  

        if not serializer.is_valid():
            return Response({Constants.MESSAGE:"Invalid phone number", Constants.PROFILE: None, Constants.IS_VERIFIED: False}, status = status.HTTP_200_OK)
        try:
            user_profile = Profile.objects.get(phone_number = phone_number)
        except Profile.DoesNotExist:
            user_profile = Profile.objects.create(phone_number = phone_number)