from blog.views import PostListView, PostDetailView, HitsListView, NewPostsListView, post_delete, PostUpdateView, \
    UrlPostCreate, ArticlePostCreate, search_list_view, tag_stats_list_view, subscribed_content
from comment.views import delete_comment, like_comment, dislike_comment
from django.urls import path, re_path
from likes.views import post_like
from subscribe.views import fav_post

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('search/', search_list_view, name='post-search'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/delete/<int:id>/', delete_comment, name='comment-delete'),
    path('post/<int:pk>/comment/like/<int:id>/', like_comment, name='comment-like'),
    path('post/<int:pk>/comment/dislike/<int:id>/', dislike_comment, name='comment-dislike'),
    path('post/delete/<int:pk>/', post_delete, name='post-delete'),
    path('post/like/<int:pk>/', post_like, name='post-like'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post/add/', UrlPostCreate.as_view(), name='post-url-create'),
    path('post/add/article/', ArticlePostCreate.as_view(), name='post-article-create'),
    path('hity/', HitsListView.as_view(), name='hity'),
    path('nowe/', NewPostsListView.as_view(), name='nowe'),
    path('obserwowane/',subscribed_content, name='subscribed_content'),
    re_path(r'^tag/(?P<slug>[\w-]+)/$', tag_stats_list_view, name='tag_stats'),
    path('post/<int:pk>/favourite/', fav_post, name='fav_post'),

]