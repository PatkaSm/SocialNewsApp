from django.urls import path, re_path
from subscribe.views import user_subscribe, user_block, tag_block, tag_subscribe, fav_post, fav_micro_post

urlpatterns = [
    re_path(r'^micro-post/(?P<pk>[0-9])/favourite/$', fav_micro_post, name='fav_micro_post'),
    re_path(r'^tag/(?P<slug>[\w-]+)/subscribe/$', tag_subscribe, name='tag-subscribe'),
    re_path(r'^tag/(?P<slug>[\w-]+)/block/$', tag_block, name='tag-block'),
    re_path(r'^user/(?P<pk>[0-9])/block/$',user_block , name='user-block'),
    re_path('user/(?P<pk>[0-9])/subscribe/$',user_subscribe , name='user-subscribe'),

]