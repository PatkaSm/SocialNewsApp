from django.contrib.auth.models import AbstractUser
from django.db import models


def upload_location(instance, filename):
    return "user %s/%s" %(instance.username, filename)


GENDER_CHOICES = (
    ('k', 'Kobieta'),
    ('m', 'Kężczyna'),
    ('n', 'Nie chcę podawać swojej płci'),
)


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(blank=True, max_length=None, default='user.png', upload_to=upload_location)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=1)
    facebook = models.CharField(max_length=500, blank=True)
    twitter = models.CharField(max_length=500, blank=True)
    ig = models.CharField(max_length=500, blank=True)
    public_email = models.EmailField(max_length=500, blank=True)
    user_page = models.CharField(max_length=500, blank=True)