from django.db.models import Count, Q
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from likes.models import Reaction
from mikroblog.forms import MicroPostForm
from mikroblog.models import MicroPost
from tag.models import Tag


class MicroPostListView(ListView, FormMixin):
    model = MicroPost
    template_name = 'microblog/microblog.html'
    context_object_name = 'posts'
    form_class = MicroPostForm

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        posts = MicroPost.objects.all().annotate(
            likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-date_posted', 'likes')
        popular_tags = Tag.objects.all().annotate(ilosc=Count('micro_posts')).order_by('-ilosc')[:20]
        popular_posts = MicroPost.objects.all().annotate(
            likes=Count('reactions', filr=Q(reactions__type=Reaction.Type.UPVOTE)))

        context = {
            'posts': posts,
            'popular_tags': popular_tags,
            'popular_posts': popular_posts,
            'micro_post_form': MicroPostForm(initial={'author': self.request.user.id,})
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return super(MicroPostListView, self).form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('mikroblog')

