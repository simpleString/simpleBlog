from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import exceptions
from django.views.generic import UpdateView
from django.db.models import Q

from .forms import *
from .models import *


def index(request):
    return render(request, 'books/main.html')


def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        user_form = UserCreationForm()
       
    return render(request, 'registration/signup.html', {'form': user_form})


@login_required
def profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if not profile:
        form = CustomProfile()
        return render(request, 'registration/profile.html', {'form': form})
    if request.method == 'POST':
        form = CustomProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('index')
    else:
        form = CustomProfile(instance=profile)
    return render(request, 'registration/profile.html', {'form': form})


def list(request):
    query = request.GET.get('q','')
    if query:
        queryset = (Q(title__icontains=query))
        posts_list = Post.objects.filter(queryset).distinct()
    else:
        posts_list = Post.objects.all()
    content = {
        "posts": posts_list
    }
    return render(request, 'books/list.html', {'content': content})


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('list')
    else:
        form = PostForm()
    return render(request, 'books/create.html', {'form': form})


def detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post_id = pk
            comment.save()
            return redirect('detail', pk=pk)
    form = CommentForm()
    return render(request, 'books/detail.html', {'post': post, 'form': form})



@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.user != request.user:
        raise exceptions.Resolver404()
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('detail', pk=pk)
    return render(request, 'books/update.html', {'form': form})


@login_required
def like_post(request, pk):
    if request.method == 'POST':
        current_post = Post.objects.get(pk=pk)
        user = get_object_or_404(UserProfile, user=request.user)
        post = user.liked_posts.filter(pk=pk).first()
        if not post:
            user.liked_posts.add(pk)
        else:
            user.liked_posts.remove(post)
        result = {'data': current_post.users.count() }
        return JsonResponse(result)

        
