
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/create/", views.new_post, name="new_post"),
    path("profile/<str:username>/", views.profile_page, name="profile_page"),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
    path("following/", views.following_page, name="following_page"),
    path("edit-post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("like/<int:post_id>/", views.toggle_like, name="toggle_like")

    
    
]
