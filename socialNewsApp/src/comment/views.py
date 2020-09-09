from comment.models import Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from likes.models import Reaction


@login_required
def delete_comment(request, pk, id):
    query = Comment.objects.get(id=id)
    query.delete()
    messages.warning(request, 'Komentarz został usunięty!')
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))


@login_required
def like_comment(request, pk, id):
    comment = Comment.objects.get(id=id)
    type = Reaction.Type.UPVOTE
    like, created = Reaction.objects.get_or_create(post_comment=comment, owner=request.user, type=type)
    if not created:
        like.delete()
    else:
        like.save()
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))


@login_required
def dislike_comment(request, pk, id):
    comment = Comment.objects.get(id=id)
    type = Reaction.Type.DOWNVOTE
    like, created = Reaction.objects.get_or_create(post_comment=comment, owner=request.user, type=type)
    if not created:
        like.delete()
    else:
        like.save()
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))


@login_required
def delete_micropost_comment(request, id):
    query = Comment.objects.get(id=id)
    query.delete()
    messages.warning(request, 'Komentarz został usunięty!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like_micropost_comment(request, id):
    comment = Comment.objects.get(id=id)
    type = Reaction.Type.UPVOTE
    like, created = Reaction.objects.get_or_create(micro_post_comment=comment, owner=request.user, type=type)
    if not created:
        like.delete()
    else:
        like.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

