from django.shortcuts import render

from django.utils import timezone
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from cbse.models import Standard
from .serializers import *

@api_view(['GET'])
def get_all_standards(request):
    if request.method == "POST":
        standards = Standard.objects.all()
        standard_serializer = StandardSerializer(standards, many = True)

        if standard_serializer.is_valid():
            return Response(standard_serializer.data, status = status.HTTP_200_OK)