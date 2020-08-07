from django.db import models
from blog.models import Post
from django.utils import timezone
from mikroblog.models import MicroPost
from user.models import User


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, related_name='comments', null=True)
    microPost = models.ForeignKey(MicroPost, on_delete=models.CASCADE, blank=True, related_name='comments', null=True)
    content = models.TextField(max_length=500)
    date_added = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)