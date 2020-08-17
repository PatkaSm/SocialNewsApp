from django import forms
from tag.models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('word', )
        widgets = {
            'word': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
