from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, over=None, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ["content", 'user','post','username']


class CommentAnonForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
