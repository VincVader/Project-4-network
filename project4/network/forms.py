from django import forms
from .models import Like, Post, User

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'content'}