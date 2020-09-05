from blog.models import Post
from django.db import models
from mikroblog.models import MicroPost
from tag.models import Tag
from user.models import User


class Subscribe(models.Model):
    class Type(models.TextChoices):
        SUB = 'sub', 'Sub'
        BLOCK = 'block', 'Block'

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=5, choices=Type.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', null=True, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_subscriptions', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favourite_posts', null=True, blank=True)
    micro_post = models.ForeignKey(MicroPost, on_delete=models.CASCADE, related_name='liked_micro_posts', null=True,
                                   blank=True)
