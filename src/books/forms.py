from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'photo',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'text',
        )


class CustomProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'liked_posts')


class CustomSignUp(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)