import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from django.core.paginator import Paginator

from .models import User, Post, Like, Follow
from .forms import NewPost


def index(request):
    
    posts = Post.objects.all()
    likes = 0
    posts = posts.order_by("-date_posted").all()
    for post in posts:
        post.likes_count = len(Like.objects.filter(post=post.pk))
        try:
            if request.user.is_authenticated:
                Like.objects.get(post=post.pk, user=request.user)
                post.liked = True
        except Like.DoesNotExist:
            post.liked = False

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        'page_obj': page_obj,        
        
    })

def profile(request, user_id):
    posts = Post.objects.filter(author=user_id).order_by("-date_posted").all()
    if request.user.is_authenticated:
        try:
            follow = Follow.objects.get(user=posts.first().author, following_user=request.user)
        except Follow.DoesNotExist:
            follow = None
    else:
        follow = None
    for post in posts:
        post.likes_count = len(Like.objects.filter(post=post.pk))
        if request.user.is_authenticated:
            try:
                Like.objects.get(post=post.pk, user=request.user)
                post.liked = True
            except Like.DoesNotExist:
                post.liked = False

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "follow": follow,
        'page_obj': page_obj,        

    })


def follow(request, user_id):
    if request.method == "POST":   
        user = User.objects.get(id=user_id)        
        if not request.user == user_id:
            try:
                f0 = Follow.objects.get(user=user, following_user=request.user)           
                f0.delete()
                return JsonResponse({"message":"Unfollowed"}, status=201)
            except Follow.DoesNotExist:
                f0 = Follow(user=user, following_user=request.user)
                f0.save()
                return JsonResponse({"message":"Followed"}, status=201)
        else:
            return JsonResponse({"message":"You can't follow yourself"}, status=201)

    elif request.method == "GET":    
        followers = len(Follow.objects.filter(user=user_id))
        following = len(Follow.objects.filter(following_user=user_id))
        if request.user.is_authenticated:
            try:
                f0 = Follow.objects.get(user=user_id, following_user=request.user)
                follow = 'Unfollow'
            except Follow.DoesNotExist:
                follow = 'Follow'
        else:
            follow = 'Sign in to follow'
    
        return JsonResponse({"follow":follow,'following': following, 'followers': followers})
     
    return JsonResponse({"message":"OK"}, status=201)
    

def following(request):
    user = User.objects.get(id=request.user.pk)
    follow = Follow.objects.filter(following_user=user)
    posts = []
    for items in follow:
        posts += Post.objects.filter(author=items.user)
        
    posts.sort(key=lambda x: x.date_posted, reverse=True)
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {        
        "follow": follow,
        'page_obj': page_obj,   
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
            return render(request, 'network/new_post.html', {
                "form": form
            })
    else:
        return render(request, 'network/new_post.html', {
        "form": form
    })

def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    edit_form = NewPost(request.POST or None, instance=post)
    if post.author != request.user:
        return HttpResponseRedirect(reverse("index"))
        
    if edit_form.is_valid():
        edit_form.save()
        return HttpResponseRedirect(reverse("index"))
    else:        
        return render(request, 'network/edit_post.html', {
        "edit_form":edit_form,
        "post_id": post_id
    })

    
def like(request):
    data = json.loads(request.body)
    user = User.objects.get(id=data.get("user"))
    post = Post.objects.get(id=data.get("post"))
    liked = data.get("liked")
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
    


def likes(request, post_id):
    if request.method == "GET":        
        try:
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
