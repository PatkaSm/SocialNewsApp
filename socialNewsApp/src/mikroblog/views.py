from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from likes.models import Reaction
from mikroblog.forms import MicroPostForm
from mikroblog.models import MicroPost
from tag.forms import TagForm
from tag.models import Tag
from django.contrib import messages


class MicroPostListView(ListView, FormMixin):
    model = MicroPost
    template_name = 'microblog/microblog.html'
    context_object_name = 'posts'
    form_class = MicroPostForm
    paginate_by = 10

    def get_queryset(self):
        return MicroPost.objects.all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data['posts'] = self.object_list.annotate(
                likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE)),
                is_liked=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE,
                                                     reactions__owner=self.request.user))).order_by('-date_posted',
                                                                                                    'likes')
        else:
            data['posts'] = self.object_list.annotate(
                likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-date_posted',
                                                                                                   'likes')
        data['popular_tags'] = Tag.objects.all().annotate(ilosc=Count('micro_posts')).order_by('-ilosc')[:20]
        data['popular_posts'] = MicroPost.objects.all().annotate(
            likes=Count('reactions', filr=Q(reactions__type=Reaction.Type.UPVOTE)))

        data['micro_post_form'] = MicroPostForm(initial={'author': self.request.user.id}),
        data['tags_form'] = TagForm()

        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form(MicroPostForm)
        tag_form = self.get_form(TagForm)
        if form.is_valid() & tag_form.is_valid():
            micropost = form.save()
            tags_data = tag_form.cleaned_data['word'].split(',')
            for word in tags_data:
                used_tag = Tag.objects.filter(word=word)
                if used_tag.exists():
                    micropost.tag.add(used_tag[0])
                else:
                    tag = Tag.objects.create(word=word)
                    micropost.tag.add(tag)
            return super(MicroPostListView, self).form_valid(form)

    def get_success_url(self):
        return reverse('mikroblog')


@login_required
def micro_post_delete(request, pk):
    micro_post = get_object_or_404(MicroPost, pk=pk)
    micro_post.delete()
    messages.warning(request, 'Wpis został usunięty!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def micro_post_like(request, pk):
    micro_post = get_object_or_404(MicroPost, pk=pk)
    type = Reaction.Type.UPVOTE
    like, created = Reaction.objects.get_or_create(micro_post=micro_post, owner=request.user, type=type)
    if not created:
        like.delete()
    else:
        like.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
