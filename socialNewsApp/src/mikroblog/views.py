from django.shortcuts import render
from django.views.generic import ListView
from mikroblog.models import MicroPost


class MicroPostListView(ListView):
    model = MicroPost
    template_name = 'microblog/microblog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

