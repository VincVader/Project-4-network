
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("liked", views.like, name="like"),
    path("new_post", views.new_post, name="new_post"),
    path("liked/<int:post_id>", views.likes, name="likes"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),    
]
