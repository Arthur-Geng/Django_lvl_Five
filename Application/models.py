from django.db import models
from django.contrib.auth.models import User  # basic user model


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=256)
    principal = models.CharField(max_length=256)
    location = models.CharField(max_length=256)

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    name = models.CharField(max_length=256)
    age = models.PositiveIntegerField()
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserProfileInfoModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return self.user.username
