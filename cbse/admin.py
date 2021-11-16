from django.contrib import admin
from django.db.models.fields import CharField

from .models import *

admin.site.register(Board)
admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Language)