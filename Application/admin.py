from django.contrib import admin
from Application.models import UserProfileInfoModel, School, Student
# Register your models here.
# admin.register(UserProfileInfoModel)

admin.site.register(UserProfileInfoModel)
admin.site.register(School)
admin.site.register(Student)