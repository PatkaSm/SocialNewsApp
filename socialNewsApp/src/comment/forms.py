from comment.models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'img', 'owner', 'post','microPost')
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'editor form-control'
            }),
            'owner': forms.HiddenInput(),
            'post': forms.HiddenInput(),
            'microPost': forms.HiddenInput(),

        }
