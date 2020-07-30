from django.db import models
from django.utils import timezone
from tag.models import Tag
from user.models import User


def upload_location(instance, filename):
    return "microPost %s/%s" %(instance.id, filename)


class MicroPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, max_length=1500)
    tag = models.ManyToManyField(Tag)
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(blank=True, max_length=None, default='user.png', upload_to=upload_location)
