from django.shortcuts import render

from nodia import Constants
from . import utils

from .serializers import *

from rest_framework.decorators import api_view

@api_view(["POST"])
def generate_otp(request):
    if request.method == "POST":
        hashValue = request.POST.get(Constants.HASH)
        phone_number = request.POST.get(Constants.PHONE_NUMBER) 

        otp = utils.otp_generator()
        serializer = OTPSerializer(data = request.data)  
