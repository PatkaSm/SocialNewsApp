from blog.models import Post
from django import forms
from likes.models import Reaction


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


class UrlPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('link', 'author',)
        widgets = {
            'author': forms.HiddenInput(),
            'link': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
