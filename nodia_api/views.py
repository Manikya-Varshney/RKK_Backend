from django.db.models import manager
from django.shortcuts import render

from nodia import Constants
from . import utils

from .serializers import *
from cbse.serializers import *
from users.serializers import *

from users.models import *
from cbse.models import *

import requests

from django.utils import timezone
from django.forms.models import model_to_dict
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

        # url = Constants.OTP_URL+ Constants.OTP_KEY+ "SMS/" + phone_number + "/" + str(otp)
        # requests.post( url )

        if user_profile:
            user_profile.otp = otp
            user_profile.save()
            message = Constants.OTP_MESSAGE + " {otp} \n {hash}".format(otp = otp, hash = hashValue)
            data = {Constants.MESSAGE: message, Constants.PROFILE: model_to_dict(user_profile), Constants.IS_VERIFIED: False}
            return Response(data, status = status.HTTP_200_OK)
        else:
            return Response({Constants.MESSAGE: 'User Does Not Exist', Constants.IS_VERIFIED: False, Constants.PROFILE: None}, status = status.HTTP_200_OK)

@api_view(['POST',])
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get(Constants.OTP)
        phone_number = request.POST.get(Constants.PHONE_NUMBER)
        serializer = OTPSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({Constants.MESSAGE:'Phone Number Not Validated!', Constants.PROFILE: None, Constants.IS_VERIFIED: False}, status = status.HTTP_404_NOT_FOUND)

        try:
            user_profile = Profile.objects.get(phone_number = phone_number)
        except Profile.DoesNotExist:
            return Response({Constants.MESSAGE: 'Profile does not exist!', Constants.PROFILE: None, Constants.IS_VERIFIED: False}, status = status.HTTP_404_NOT_FOUND)

        if user_profile:
            if otp == str(user_profile.otp) :
                if (timezone.now() - user_profile.otp_timestamp).seconds < 1800:
                    data = {Constants.MESSAGE: 'OTP Verified Successfully!', Constants.PROFILE: model_to_dict(user_profile), Constants.IS_VERIFIED: True}
                    return Response(data, status = status.HTTP_200_OK)
                else:
                    return Response({Constants.MESSAGE: 'OTP has expired!', Constants.PROFILE: model_to_dict(user_profile), Constants.IS_VERIFIED: False}, status = status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({Constants.MESSAGE: 'OTP Verification Failed!. The entered OTP is incorrect', Constants.PROFILE: model_to_dict(user_profile), Constants.IS_VERIFIED: False}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def get_all_boards(request):
    if request.method == "GET":
        boards = Board.objects.all()
        board_serializer = BoardSerializer(boards, many = True)
        return Response(board_serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def get_all_standards(request):
    if request.method == "GET":
        board_id = request.GET.get('board_id', 1)
        standards = Standard.objects.filter(boards__id = board_id)
        standard_serializer = StandardSerializer(standards, many = True)
        return Response(standard_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_all_subjects(request):
    if request.method == "GET":
        standard_id = request.GET.get('standard_id', 1)
        subjects = Subject.objects.filter(standards__id = standard_id)
        subject_serializer = SubjectSerializer(subjects, many = True)
        return Response(subject_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_all_chapters(request):
    if request.method == "GET":
        subject_id = request.GET.get('subject_id', 2)
        chapters = Chapter.objects.filter(subject__id = subject_id)
        chapter_serializer = ChapterSerializer(chapters, many = True)
        return Response(chapter_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_all_languages(request):
    if request.method == "GET":
        board_id = request.GET.get('board_id', 1)
        languages = Language.objects.filter(boards__id = board_id)
        language_serializer = LanguageSerializer(languages, many = True)
        return Response(language_serializer.data, status = status.HTTP_200_OK)

@api_view(['POST',])
def update_profile(request):
    if request.method == "POST":
        profile = Profile.objects.get(id = request.POST.get('id'))
        print(request.data)
        profile_serializer = ProfileSerializer(profile, data = request.data)
        print(repr(profile_serializer))
        if not profile_serializer.is_valid():
            print(profile_serializer.errors)
            return Response({Constants.MESSAGE: 'Invalid data', Constants.PROFILE: None}, status = status.HTTP_400_BAD_REQUEST)

        updated_profile = profile_serializer.save()
        return Response({Constants.MESSAGE: 'Profile update successfully', Constants.PROFILE: model_to_dict(updated_profile)}, status = status.HTTP_200_OK)
