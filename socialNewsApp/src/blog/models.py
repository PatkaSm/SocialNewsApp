from django.db import models
from django.utils import timezone
from tag.models import Tag
from user.models import User
from bs4 import BeautifulSoup
import requests


def upload_location(instance, filename):
    return "post %s/%s" % (instance.id, filename)


class Post(models.Model):
    class Type(models.TextChoices):
        URL = "url", "Url"
        TEXT = "txt", "Tekstowy"

    type = models.CharField(max_length=5, choices=Type.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.ManyToManyField(Tag, related_name='posts')
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(blank=True, null=True, max_length=None, upload_to=upload_location)
    imag_url = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

