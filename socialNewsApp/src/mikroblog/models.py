from django.db import models
from django.utils import timezone
from tag.models import Tag
from user.models import User


class MicroPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.ManyToManyField(Tag)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

