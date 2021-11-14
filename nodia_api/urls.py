from django.urls import path

from .views import *

urlpatterns = [
    path('generate_otp', generate_otp, name = 'generate_otp'),
    path('verify_otp', verify_otp, name = 'verify_otp'),
    path('get_all_boards', get_all_boards, name = 'get_all_boards'),
    path('get_all_standards', get_all_standards, name = 'get_all_standards')
]