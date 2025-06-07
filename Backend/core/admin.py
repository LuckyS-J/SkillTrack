from django.contrib import admin
from .models import Skill, StudySession, UserProfile, Address

# Register your models here.

admin.site.register(Skill)
admin.site.register(StudySession)
admin.site.register(UserProfile)
admin.site.register(Address)
