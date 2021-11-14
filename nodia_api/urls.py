from django.urls import path

from .views import *

urlpatterns = [
    path('generate_otp', generate_otp, name = 'generate_otp')
]