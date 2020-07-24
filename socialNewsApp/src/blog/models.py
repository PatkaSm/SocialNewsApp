from django.db import models
from django.utils import timezone
from tag.models import Tag
from user.models import User


def upload_location(instance, filename):
    return "user %s/%s" %(instance.id, filename)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.ManyToManyField(Tag)
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(blank=True, max_length=None, default='user.png', upload_to=upload_location)

    def __str__(self):
        return self.title
