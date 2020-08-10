from django.db.models import Count, Q
from django.views.generic import ListView
from likes.models import Reaction
from mikroblog.models import MicroPost
from tag.models import Tag


class MicroPostListView(ListView):
    model = MicroPost
    template_name = 'microblog/microblog.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        posts = MicroPost.objects.all().annotate(
            likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-date_posted', 'likes')
        popular_tags = Tag.objects.all().annotate(ilosc=Count('micro_posts')).order_by('-ilosc')[:20]
        popular_posts = MicroPost.objects.all().annotate(
            likes=Count('reactions', filr=Q(reactions__type=Reaction.Type.UPVOTE)))

        context = {
            'posts': posts,
            'popular_tags': popular_tags,
            'popular_posts': popular_posts
        }
        return context
