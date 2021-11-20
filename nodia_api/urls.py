from django.urls import path

from .views import *

urlpatterns = [
    path('generate_otp', generate_otp, name = 'generate_otp'),
    path('verify_otp', verify_otp, name = 'verify_otp'),
    path('get_all_boards', get_all_boards, name = 'get_all_boards'),
    path('get_all_standards', get_all_standards, name = 'get_all_standards'),
    path('get_all_subjects', get_all_subjects, name = 'get_all_subjects'),
    path('get_all_chapters', get_all_chapters, name = 'get_all_chapters'),
    path('get_all_languages', get_all_languages, name = "get_all_languages"),
    path('update_profile', update_profile, name = "update_profile"),
    path('get_all_plans', get_all_plans, name = "get_all_plans"),
    path('get_my_subjects', get_my_subjects, name = "get_my_subjects"),
    path('update_plan', update_plan, name = "update_plan")

]
