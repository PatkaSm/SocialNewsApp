from comment.models import Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


@login_required(login_url="/")
def delete_comment(request, pk, id):
    query = Comment.objects.get(id=id)
    query.delete()
    messages.warning(request, 'Komentarz został usunięty!')
    return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': pk}))
