from typing import cast
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
        print(Constants.TEMPLATE_NAME)
        url = Constants.OTP_URL + Constants.OTP_KEY + "SMS" + "/" + phone_number + "/" + str(otp) + "/" +  Constants.TEMPLATE_NAME
        requests.post( url )

        if user_profile:
            user_profile.otp = otp
            user_profile.save()
            profile_serializer = ProfileSerializer(user_profile)
            message = Constants.OTP_MESSAGE + " {otp} \n {hash}".format(otp = otp, hash = hashValue)
            data = {Constants.MESSAGE: message, Constants.PROFILE: profile_serializer.data, Constants.IS_VERIFIED: False}
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
            profile_serializer = ProfileSerializer(user_profile)
            if otp == str(user_profile.otp) :
                if (timezone.now() - user_profile.otp_timestamp).seconds < 1800:
                    data = {Constants.MESSAGE: 'OTP Verified Successfully!', Constants.PROFILE: profile_serializer.data, Constants.IS_VERIFIED: True}
                    return Response(profile_serializer.data, status = status.HTTP_200_OK)
                else:
                    return Response({Constants.MESSAGE: 'OTP has expired!', Constants.PROFILE: profile_serializer.data, Constants.IS_VERIFIED: False}, status = status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({Constants.MESSAGE: 'OTP Verification Failed!. The entered OTP is incorrect', Constants.PROFILE: profile_serializer.data, Constants.IS_VERIFIED: False}, status = status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def get_all_boards(request):
    if request.method == "GET":
        boards = Board.objects.all()
        board_serializer = BoardSerializer(boards, many = True)
        return Response(board_serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def get_all_standards(request):
    if request.method == "GET":
        board_id = request.GET.get('board_id', None)
        if board_id:
            try:
                board = Board.objects.get(id = board_id)
                standards = board.standards.all()
                # standards = Standard.objects.filter(board__id = board_id)
            except:
                return Response({}, status = status.HTTP_404_NOT_FOUND)

        else:
            standards = Standard.objects.all()
        standard_serializer = StandardSerializer(standards, many = True)
        return Response(standard_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_all_subjects(request):
    if request.method == "GET":
        standard_id = request.GET.get('standard_id', None)
        if standard_id:
            try:
                standard = Standard.objects.get(id = standard_id)
                subjects = standard.subjects.all()
                # subjects = Subject.objects.filter(standards__id = standard_id)
            except:
                return Response({}, status = status.HTTP_404_NOT_FOUND)

        else:
            subjects = Subject.objects.all()
        subject_serializer = SubjectSerializer(subjects, many = True)
        return Response(subject_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_all_chapters(request):
    if request.method == "GET":
        subject_id = request.GET.get('subject_id', None)
        if subject_id:
            try:
                subject = Subject.objects.get(id = subject_id)
                chapters = subject.chapters.all()
                # chapters = Chapter.objects.filter(subject__id = subject_id)
            except:
                return Response({}, status = status.HTTP_404_NOT_FOUND)

        else:
            chapters = Chapter.objects.all()
        chapter_serializer = ChapterSerializer(chapters, many = True)
        return Response(chapter_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_all_languages(request):
    if request.method == "GET":
        board_id = request.GET.get('board_id', None)
        if board_id:
            try:
                board = Board.objects.get(id = board_id)
                languages = board.languages.all()
                # languages = Language.objects.filter(boards__id = board_id)
            except:
                return Response({}, status = status.HTTP_404_NOT_FOUND)

        else:
            languages = Language.objects.all()
        language_serializer = LanguageSerializer(languages, many = True)
        return Response(language_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_all_plans(request):
    if request.method == "GET":
        plans = Plan.objects.all()
        plan_serializer = PlanSerializer(plans, many = True)
        return Response(plan_serializer.data, status = status.HTTP_200_OK)

@api_view(['POST',])
def update_profile(request):
    if request.method == "POST":
        print(request.data)
        profile = Profile.objects.get(phone_number = request.data.get('phone_number'))
        profile_serializer = ProfileSerializer(profile, data = request.data)
        if not profile_serializer.is_valid():
            print(profile_serializer.errors)
            return Response({Constants.MESSAGE: 'Invalid data', Constants.PROFILE: None}, status = status.HTTP_400_BAD_REQUEST)

        updated_profile = profile_serializer.save()
        return Response(profile_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_my_subjects(request):
    if request.method == "GET":
        phone_number = request.GET.get('phone_number', None)
        subjects = None
        if phone_number:
            try:
                profile = Profile.objects.get(phone_number = phone_number)
                subjects = profile.subjects.all()
            except:
                return Response({Constants.MESSAGE: "No subjects found"}, status = status.HTTP_404_NOT_FOUND)

        if subjects is None:
            return Response({Constants.MESSAGE: "No subjects found"}, status = status.HTTP_404_NOT_FOUND)

        subject_serializer = SubjectSerializer(subjects, many = True)

        return Response(subject_serializer.data, status = status.HTTP_200_OK)

@api_view(['POST'])
def update_plan(request):
    if request.method == "POST":
        plan_id = request.POST.get('plan_id', None)
        phone_number = request.POST.get('phone_number', None)

        try:
            profile = Profile.objects.get(phone_number = phone_number)
        except:
             return Response({Constants.MESSAGE: "Profile not found"}, status = status.HTTP_404_NOT_FOUND)

        try:
            plan = Plan.objects.get(id = plan_id)
        except:
             return Response({Constants.MESSAGE: "Plan does not exist"}, status = status.HTTP_404_NOT_FOUND)

        profile.plan = plan
        profile.plan_start_date = timezone.now()
        profile.save()

        profile_serializer = ProfileSerializer(profile)
        print(profile_serializer.data)
        return Response(profile_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_profile(request):
    if request.method == "GET":
        phone_number = request.GET.get('phone_number', None)

        if phone_number:
            try:
                profile = Profile.objects.get(phone_number = phone_number)
            except:
                return Response({Constants.MESSAGE: "No user found"}, status = status.HTTP_400_BAD_REQUEST)

            profile_serializer = ProfileSerializer(profile)

            return Response(profile_serializer.data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_chapter_documents(request):
    if request.method == "GET":
        phone_number = request.GET.get('phone_number', None)
        chapter_id = request.GET.get('chapter_id', None)

        try:
            chapter = Chapter.objects.get(id = chapter_id)
            chapter_documents = chapter.documents.all().order_by('rank')
            chapter_documents_serializer = ChapterDocumentsSerializer(chapter_documents, many = True)
            return Response(chapter_documents_serializer.data, status = status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({Constants.MESSAGE:"Chapter does not exist"}, status = status.HTTP_404_NOT_FOUND)
