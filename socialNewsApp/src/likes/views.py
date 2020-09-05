from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from likes.models import Reaction


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    type = Reaction.Type.UPVOTE
    like, created = Reaction.objects.get_or_create(post=post, owner=request.user, type=type)
    if not created:
        like.delete()
    else:
        like.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
