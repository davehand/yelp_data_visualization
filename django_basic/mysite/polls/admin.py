from django.contrib import admin
from django.contrib import admin
from polls.models import Question
from polls.models import Choice

# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)
