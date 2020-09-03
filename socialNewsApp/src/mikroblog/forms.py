from django import forms
from mikroblog.models import MicroPost


class MicroPostForm(forms.ModelForm):

    class Meta:
        model = MicroPost
        fields = ('content', 'image', 'author')
        widgets = {
            'author': forms.HiddenInput(),
            'content': forms.HiddenInput(),

        }
