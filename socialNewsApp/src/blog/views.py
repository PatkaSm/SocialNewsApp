from blog.forms import PostUpdateForm, UrlPostForm
from comment.forms import CommentForm
from comment.models import Comment
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, UpdateView, CreateView
from likes.models import Reaction
from datetime import datetime, timedelta
from mikroblog.models import MicroPost
from tag.forms import TagForm
from tag.models import Tag
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        posts = Post.objects.all().annotate(
            likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE)),
            is_liked=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE,
                                                 reactions__owner=self.request.user))).order_by(
            '-date_posted', '-likes')
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
        post_data = self.object
        is_liked = Reaction.objects.filter(owner=self.request.user, post=post_data).count()
        post_reactions_upvote = post_data.reactions.filter(type=Reaction.Type.UPVOTE).count()
        post_reactions_down_vote = post_data.reactions.filter(type=Reaction.Type.DOWNVOTE).count()
        similar_posts = Post.objects.annotate(
            likes=Count('reactions', filter=(Q(reactions__type=Reaction.Type.UPVOTE)))).filter(
            tag__in=post_data.tag.all()).exclude(id=post_data.id).distinct().order_by('-likes')[:6]
        post_comments = Comment.objects.filter(post=post_data).annotate(
            likes=Count('post_comment_reactions', filter=Q(post_comment_reactions__type=Reaction.Type.UPVOTE)),
            dislikes=Count('post_comment_reactions', filter=Q(post_comment_reactions__type=Reaction.Type.DOWNVOTE)),
            is_liked=Count('post_comment_reactions', filter=Q(post_comment_reactions__type=Reaction.Type.UPVOTE,
                                                 post_comment_reactions__owner=self.request.user)),
            is_disliked=Count('post_comment_reactions', filter=Q(post_comment_reactions__type=Reaction.Type.DOWNVOTE,
                                                 post_comment_reactions__owner=self.request.user))
        )

        context = {
            'post': post_data,
            'is_liked':is_liked,
            'post_up_vote': post_reactions_upvote,
            'post_down_vote': post_reactions_down_vote,
            'similar_posts': similar_posts,
            'post_comments': post_comments,
            'comment_form': CommentForm(initial={'post': self.object, 'owner': self.request.user.id}),
            'comments': post_comments.count(),
        }
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, 'Komentarz został dodany!')
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
            likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE)),
            is_liked=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE,
                                                 reactions__owner=self.request.user))).order_by('-likes')
        popular_comments = Comment.objects.annotate(
            likes=Count('post_comment_reactions',
                        filter=(Q(post_comment_reactions__type=Reaction.Type.UPVOTE)))).order_by('-likes')[:10]

        context = {
            'posts': posts,
            'popular_comments': popular_comments
        }
        return context


class NewPostsListView(ListView):
    model = Post
    template_name = 'blog/news.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        posts = Post.objects.filter(date_posted__gte=datetime.now() - timedelta(days=1)).annotate(
            likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE)),
            is_liked=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE,
                                                 reactions__owner=self.request.user))).order_by('-date_posted')
        popular_posts = posts.order_by('-likes')[:10]

        context = {
            'posts': posts,
            'popular_posts': popular_posts
        }
        return context


class UrlPostCreate(CreateView):
    model = Post
    template_name = 'blog/new_post.html'
    form_class = UrlPostForm

    def get_context_data(self, **kwargs):
        context = super(UrlPostCreate, self).get_context_data(**kwargs)
        context['tag_form'] = TagForm()
        return context

    def get_initial(self):
        initial = super(UrlPostCreate, self).get_initial()
        initial = initial.copy()
        initial['author'] = self.request.user.pk
        return initial

    def form_valid(self, form):
        form = self.get_form(UrlPostForm)
        tag_form = self.get_form(TagForm)
        if form.is_valid() & tag_form.is_valid():
            url_post = form.save()
            tags_data = tag_form.cleaned_data['word'].split(',')
            for word in tags_data:
                used_tag = Tag.objects.filter(word=word)
                if used_tag.exists():
                    url_post.tag.add(used_tag[0])
                else:
                    tag = Tag.objects.create(word=word)
                    url_post.tag.add(tag)
            return super(UrlPostCreate, self).form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('blog-home')


class ArticlePostCreate(CreateView):
    model = Post
    template_name = 'blog/new_text_post.html'
    form_class = PostUpdateForm

    def get_context_data(self, **kwargs):
        context = super(ArticlePostCreate, self).get_context_data(**kwargs)
        context['tag_form'] = TagForm()
        return context

    def get_success_url(self):
        return reverse('blog-home')

    def get_initial(self):
        initial = super(ArticlePostCreate, self).get_initial()
        initial = initial.copy()
        initial['author'] = self.request.user.pk
        return initial

    def form_valid(self, form):
        form = self.get_form(ArticlePostCreate)
        tag_form = self.get_form(TagForm)
        if form.is_valid() & tag_form.is_valid():
            url_post = form.save()
            tags_data = tag_form.cleaned_data['word'].split(',')
            for word in tags_data:
                used_tag = Tag.objects.filter(word=word)
                if used_tag.exists():
                    url_post.tag.add(used_tag[0])
                else:
                    tag = Tag.objects.create(word=word)
                    url_post.tag.add(tag)
            return super(ArticlePostCreate, self).form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostUpdateForm

    def get_context_data(self, **kwargs):
        post_data = self.object
        post_reactions_upvote = post_data.reactions.filter(type=Reaction.Type.UPVOTE).count()
        post_reactions_down_vote = post_data.reactions.filter(type=Reaction.Type.DOWNVOTE).count()

        context = {
            'post': post_data,
            'post_up_vote': post_reactions_upvote,
            'post_down_vote': post_reactions_down_vote,
            'form': self.get_form(),
        }
        return context

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})


def search_list_view(request):
    template = 'blog/post_search.html'
    word = request.GET.get('szukaj')
    if word:
        posts_query = Post.objects.filter(tag__word=word)
        micro_posts_query = MicroPost.objects.filter(tag__word=word)
    else:
        posts_query = Post.objects.all()
        micro_posts_query = MicroPost.objects.all()

    posts = posts_query.annotate(
        likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-likes')
    micro_posts = micro_posts_query.annotate(
        likes=Count('reactions', filter=Q(reactions__type=Reaction.Type.UPVOTE))).order_by('-likes')

    context = {
        'posts': posts,
        'micro_posts': micro_posts
    }
    return render(request, template, context)


def post_delete(request, pk):
    query = Post.objects.get(id=pk)
    query.delete()
    messages.warning(request, 'Post został usunięty!')
    return HttpResponseRedirect(reverse('blog-home'))


def post_like(request, pk):
    post = Post.objects.get(id=pk)
    type = Reaction.Type.UPVOTE
    like, created = Reaction.objects.get_or_create(post=post, owner=request.user, type=type)
    if not created:
        like.delete()
    else:
        like.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

