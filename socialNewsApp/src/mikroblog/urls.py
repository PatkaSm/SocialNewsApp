from comment.views import delete_micropost_comment, like_micropost_comment, dislike_micropost_comment
from django.urls import path
from mikroblog.views import MicroPostListView, micro_post_delete, micro_post_like

urlpatterns = [
    path('', MicroPostListView.as_view(), name='mikroblog'),
    path('mikro-post/delete/<int:pk>',micro_post_delete , name='micro-post-delete'),
    path('mikro-post/like/<int:pk>', micro_post_like, name='micro-post-like'),
    path('wpis/<int:pk>/comment/delete/<int:id>/', delete_micropost_comment, name='micropost-comment-delete'),
    path('wpis/<int:pk>/comment/like/<int:id>/', like_micropost_comment, name='micropost-comment-like'),
    path('wpis/<int:pk>/comment/dislike/<int:id>/', dislike_micropost_comment, name='micropost-comment-dislike'),
]