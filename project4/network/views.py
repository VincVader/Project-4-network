import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like
from .forms import NewPost


def index(request):
    
    posts = Post.objects.all()
    likes = 0
    posts = posts.order_by("-date_posted").all()
    for post in posts:
        post.likes_count = len(Like.objects.filter(post=post.pk))
        if request.user.is_authenticated:
            try:
                Like.objects.get(post=post.pk, user=request.user)
                post.liked = True
            except Like.DoesNotExist:
                post.liked = False
        
        
    return render(request, "network/index.html", {
        'posts': posts,
        "likes": likes,
        
    })

def profile(request, user_id):
    posts = Post.objects.filter(author=user_id)
    likes = 0
    posts = posts.order_by("-date_posted").all()
    for post in posts:
        post.likes_count = len(Like.objects.filter(post=post.pk))
        if request.user.is_authenticated:
            try:
                Like.objects.get(post=post.pk, user=request.user)
                post.liked = True
            except Like.DoesNotExist:
                post.liked = False
    return render(request, "network/profile.html", {
        "posts": posts,
        "likes": likes,

    })

@login_required
def new_post(request):
    form = NewPost()
    if request.method == 'POST':
        post_form = NewPost(request.POST)
        if post_form.is_valid():
            created_post = post_form.save(commit=False)
            created_post.author = request.user
            created_post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            print('bruh')
            return render(request, 'network/new_post.html', {
                "form": form
            })
    else:
        return render(request, 'network/new_post.html', {
        "form": form
    })
    
@csrf_exempt
@login_required
def like(request):
    data = json.loads(request.body)
    user = User.objects.get(id=data.get("user"))
    post = Post.objects.get(id=data.get("post"))
    liked = data.get("liked")
    print(liked)
    if liked==True:        
        like = Like.objects.get(post=post, user=user)
        like.delete()    
        return JsonResponse({"message": "Unliked."}, status=201)  
    elif liked==False:
        try:
            Like.objects.get(post=post,user=user)
        except Like.DoesNotExist:
            like = Like.objects.create(post=post, user=user) 
        return JsonResponse({"message": "Liked."}, status=201)   
    return JsonResponse({"message": "Email sent successfully."}, status=201)
    
@csrf_exempt
@login_required
def likes(request, post_id):
    if request.method == "GET":        
        try:
            user = User.objects.get(id=request.user.pk)
            post = Post.objects.get(id=post_id)
            likes = Like.objects.filter(post=post)
            data = len(likes)
            return JsonResponse({'data': data})
        
        except Like.DoesNotExist:
            data = 0;
            return JsonResponse({'data': data})

    return JsonResponse({"message": "Wrong"}, status=201)

def login_view(request):
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
