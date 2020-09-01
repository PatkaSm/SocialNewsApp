from django.db import models
from django.utils import timezone
from tag.models import Tag
from user.models import User
from bs4 import BeautifulSoup
import requests
from ckeditor.fields import RichTextField


def upload_location(instance, filename):
    return "post %s/%s" % (instance.id, filename)


class Post(models.Model):
    class Type(models.TextChoices):
        URL = "url", "Url"
        TEXT = "txt", "Tekstowy"

    type = models.CharField(max_length=5, choices=Type.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    tag = models.ManyToManyField(Tag, related_name='posts')
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(blank=True, null=True, max_length=None, upload_to=upload_location)
    image_url = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.link:
            soup = BeautifulSoup(requests.get(self.link).content, 'html')
            meta = soup.find_all('meta')
            for tag in meta:
                if 'property' in tag.attrs and tag.attrs['property'].lower() in ['og:title', 'title']:
                    self.title = tag.attrs['content']
                if 'property' in tag.attrs and tag.attrs['property'].lower() in ['og:description', 'description']:
                    if len(tag.attrs['content']) > 10:
                        self.content = tag.attrs['content']
                if 'name' in tag.attrs and tag.attrs['name'].lower() in ['og:description', 'description']:
                    if len(tag.attrs['content']) > 10:
                        self.content = tag.attrs['content']
                if 'property' in tag.attrs and tag.attrs['property'].lower() in ['og:image']:
                    self.image_url = tag.attrs['content']
        super(Post, self).save(*args, **kwargs)
