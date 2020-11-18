from os import name
from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('signup', signup, name='signup'),
    path('profile', profile, name='profile'),
    path('list', list, name='list'),
    path('create', create, name='create'),
    path('detail/<int:pk>', detail, name='detail'),
    path('update/<int:pk>', update_post, name='update'),
    path('like/<int:pk>', like_post, name='likes')
]