from blog.models import Post
from django.db import models
from mikroblog.models import MicroPost
from user.models import User


class Reaction(models.Model):
    class Type(models.TextChoices):
        UPVOTE = 'up', 'Up'
        DOWNVOTE = 'down', 'Down'

    type = models.CharField(max_length=4, choices=Type.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='reactions')
    micro_post = models.ForeignKey(MicroPost, on_delete=models.CASCADE, blank=True, null=True, related_name='reactions')