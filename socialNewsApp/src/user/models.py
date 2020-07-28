
from django.contrib.auth.models import AbstractUser
from django.db import models


def upload_location(instance, filename):
    return "user %s/%s" %(instance.username, filename)


class User(AbstractUser):
    class Genders(models.IntegerChoices):
        WOMEN = '0', 'Kobieta'
        MEN = '1', 'Mężczyza'
        NONE = '2', 'Niwuadu'

    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(blank=True, max_length=None, default='user.png', upload_to=upload_location)
    background = models.ImageField(blank=True, null=True,  max_length=None, upload_to=upload_location)
    gender = models.IntegerField(choices=Genders.choices, blank=True)
    facebook = models.CharField(max_length=500, blank=True)
    twitter = models.CharField(max_length=500, blank=True)
    ig = models.CharField(max_length=500, blank=True)
    public_email = models.EmailField(max_length=500, blank=True)
    user_page = models.CharField(max_length=500, blank=True)


