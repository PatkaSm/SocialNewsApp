from django.db.models import Count, Q
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from likes.models import Reaction
from mikroblog.forms import MicroPostForm
from mikroblog.models import MicroPost
from tag.forms import TagForm
from tag.models import Tag


class MicroPostListView(ListView, FormMixin):
    model = MicroPost
    template_name = 'microblog/microblog.html'
    context_object_name = 'posts'
    form_class = MicroPostForm

    def get_context_data(self, **kwargs):
        word = self.request.GET.get('szukaj')
        if word:
            query = MicroPost.objects.filter(tag__word=word)
        else:
            query = MicroPost.objects.all()
        posts = query.annotate(
            likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-date_posted', 'likes')
        popular_tags = Tag.objects.all().annotate(ilosc=Count('micro_posts')).order_by('-ilosc')[:20]
        popular_posts = MicroPost.objects.all().annotate(
            likes=Count('reactions', filr=Q(reactions__type=Reaction.Type.UPVOTE)))

        context = {
            'posts': posts,
            'popular_tags': popular_tags,
            'popular_posts': popular_posts,
            'micro_post_form': MicroPostForm(initial={'author': self.request.user.id}),
            'tags_form': TagForm()
        }
        return context

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
        else:
            print(form.errors)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('mikroblog')

