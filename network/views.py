from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Profile


def index(request):
    posts = Post.objects.all().order_by("-timestamp")

    paginator = Paginator(posts,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj":page_obj
    })

    


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
    
@login_required
def new_post(request):
    if request.method =="POST":
        content = request.POST.get("content")

        if content.strip():
            Post.objects.create(
                user = request.user,
                content = content
            )
    return redirect("index")

def profile_page(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)

    profile_posts = Post.objects.filter(user=profile.user).order_by("-timestamp")

    is_following = False

    if request.user.is_authenticated and request.user != profile_user:
        is_following = profile.followers.filter(id=request.user.id).exists()




    context = {
        "profile_user": profile_user,
        "profile": profile,
        "profile_posts": profile_posts,
        "is_following": is_following
    }

    return render(request, "network/profile.html", context)

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile

    if request.user != target_user:
        if target_profile.followers.filter(id=request.user.id).exists():
            target_profile.followers.remove(request.user)
        else:
            target_profile.followers.add(request.user)



    return redirect("profile_page", username=username)

@login_required
def following_page(request):
    following_posts = (
        Post.objects.filter(user__profile__followers=request.user)
        .order_by("-timestamp")
    )

    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

@login_required
def edit_post(request, post_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request method"},
            status=405
        )

    
    
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return JsonResponse(
            { "error": "Permission denied"},
            status=403
            
        )
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    new_content = data.get("content").strip()

    if not new_content:
        return JsonResponse(
            {"error": "Content cannot be empty"},
            status=400
        )
    
    post.content = new_content
    post.save()

    return JsonResponse({
        "success": True,
        "content": post.content
    })


def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes": post.likes.count()
    })
    










    

