from django.db.models import Count, Q
from django.views.generic import ListView, DetailView
from likes.models import Reaction

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'


class HitsListView(ListView):
    model = Post
    template_name = 'blog/hits.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().annotate(
            likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-likes')
