from comment.models import Comment
from django.db.models import Count, Q
from django.views.generic import ListView, DetailView
from likes.models import Reaction

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    queryset = Post.objects.all().annotate(likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE)))


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'

    def get_context_data(self, **kwargs):
        post_data = kwargs['object']
        post_reactions_upvote = post_data.reactions.filter(type=Reaction.Type.UPVOTE).count()
        post_reactions_down_vote = post_data.reactions.filter(type=Reaction.Type.DOWNVOTE).count()
        similar_posts = Post.objects.annotate(
            likes=Count('reactions', filter=(Q(reactions__type=Reaction.Type.UPVOTE)))).filter(
            tag__in=post_data.tag.all()).exclude(id=post_data.id).distinct().order_by('-likes')[:6]
        post_comments = Comment.objects.filter(post=post_data).annotate(
            likes=Count('post_comment_reactions', filter=Q(post_comment_reactions__type=Reaction.Type.UPVOTE)),
            dislikes=Count('post_comment_reactions', filter=Q(post_comment_reactions__type=Reaction.Type.DOWNVOTE)),
        )

        context = {
            'post': post_data,
            'post_up_vote': post_reactions_upvote,
            'post_down_vote': post_reactions_down_vote,
            'similar_posts': similar_posts,
            'post_comments': post_comments
        }
        return context


class HitsListView(ListView):
    model = Post
    template_name = 'blog/hits.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().annotate(
        likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-likes')
