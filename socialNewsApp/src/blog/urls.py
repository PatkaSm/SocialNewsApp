from blog.views import PostListView, PostDetailView, HitsListView, NewPostsListView, post_delete, PostUpdateView
from comment.views import delete_comment
from django.urls import path
from mikroblog.views import MicroPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/delete/<int:id>/', delete_comment, name='comment-delete'),
    path('post/delete/<int:pk>', post_delete, name='post-delete'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='post-update'),
    path('mikroblog/', MicroPostListView.as_view(), name='mikroblog'),
    path('hity/', HitsListView.as_view(), name='hity'),
    path('nowe/', NewPostsListView.as_view(), name='nowe'),

]