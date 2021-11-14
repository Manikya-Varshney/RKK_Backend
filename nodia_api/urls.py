from django.urls import path

from .views import *

urlpatterns = [
    path('generate_otp', generate_otp, name = 'generate_otp'),
    path('verify_otp', verify_otp, name = 'verify_otp')
]