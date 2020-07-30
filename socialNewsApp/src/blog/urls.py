from blog.views import PostListView, PostDetailView, HitsListView
from django.urls import path
from mikroblog.views import MicroPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('mikroblog/', MicroPostListView.as_view(), name='mikroblog'),
    path('hity/', HitsListView.as_view(), name='hity'),

]