from django import forms
from tag.models import Tag


class TagForm(forms.ModelForm):
    word = forms.CharField(label='Tagi',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                           }))

    class Meta:
        model = Tag
        fields = ['word']
