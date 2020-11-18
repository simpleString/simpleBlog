from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from pathlib import Path

from ckeditor.fields import RichTextField

class Tag(models.Model):
    name =  models.CharField(max_length=120)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='profile')
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='profile_image', blank=True, default='default.png', null=True)
    liked_posts = models.ManyToManyField("Post", related_name='users')
    # is_liked = models.BooleanField(blank=True, null=True)

    @property
    def image_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            path = Path(settings.MEDIA_ROOT).relative_to(settings.BASE_DIR)
            return path / 'default.png'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120)
    content = RichTextField(blank=False)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    date_created = models.DateTimeField(auto_now_add=True)
    
    @property
    def rate(self):
        return self.users.count()
    # rate = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()