from django.contrib import admin
from polls.models import Poll, Choice, Question


admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Poll)
