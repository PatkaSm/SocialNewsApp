from comment.forms import CommentForm
from comment.models import Comment
from django.db.models import Count, Q
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from likes.models import Reaction

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        posts = Post.objects.all().annotate(likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE)))
        popular_posts = Post.objects.annotate(
            likes=Count('reactions', filter=(Q(reactions__type=Reaction.Type.UPVOTE)))).order_by('-likes',
                                                                                                 'date_posted')[:6]

        context = {
            'posts': posts,
            'popular_posts': popular_posts
        }
        return context


class PostDetailView(DetailView, FormMixin):
    model = Post
    template_name = 'blog/post_details.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        post_data = kwargs['object']
        print(post_data)
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
            'post_comments': post_comments,
            'comment_form': CommentForm(initial={'post': self.object, 'owner': self.request.user.id}),
            'comments': post_comments.count()
        }
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return super(PostDetailView, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})


class HitsListView(ListView):
    model = Post
    template_name = 'blog/hits.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        posts = Post.objects.all().annotate(
            likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-likes')
        popular_comments = Comment.objects.annotate(
            likes=Count('post_comment_reactions',
                        filter=(Q(post_comment_reactions__type=Reaction.Type.UPVOTE)))).order_by('-likes')[:10]

        context = {
            'posts': posts,
            'popular_comments': popular_comments
        }
        return context
