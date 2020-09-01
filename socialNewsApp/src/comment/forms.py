from comment.models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'img', 'owner', 'post')
        widgets = {
            'content': forms.Textarea(attrs={

            }),
            'owner': forms.HiddenInput(),
            'post': forms.HiddenInput(),
        }
