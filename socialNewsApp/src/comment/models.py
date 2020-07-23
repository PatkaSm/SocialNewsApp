from django.db import models

from blog.models import Post
from user.models import User


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    microPost = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    content = models.TextField(max_length=500)
    date_added = models.DateField(auto_now=True)
    parent = models.ForeignKey('self', blank=True, related_name='children', on_delete=models.CASCADE)