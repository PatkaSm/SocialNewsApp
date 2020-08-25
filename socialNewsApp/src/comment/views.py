from comment.models import Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from likes.models import Reaction


@login_required(login_url="/")
def delete_comment(request, pk, id):
    query = Comment.objects.get(id=id)
    query.delete()
    messages.warning(request, 'Komentarz został usunięty!')
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))


@login_required(login_url="/")
def like_comment(request, pk, id):
    comment = Comment.objects.get(id=id)
    type = Reaction.Type.UPVOTE
    like, created = Reaction.objects.get_or_create(post_comment=comment, owner=request.user, type=type)
    if not created:
        like.delete()
    else:
        like.save()
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))


@login_required(login_url="/")
def dislike_comment(request, pk, id):
    comment = Comment.objects.get(id=id)
    type = Reaction.Type.DOWNVOTE
    like, created = Reaction.objects.get_or_create(post_comment=comment, owner=request.user, type=type)
    if not created:
        like.delete()
    else:
        like.save()
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))