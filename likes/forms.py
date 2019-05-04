from django import forms
from core.models import Like


class LikeForm(forms.ModelForm):
    class Meta:
        fields = ("post", "profil")
        model = Like
