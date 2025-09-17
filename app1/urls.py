from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = "app1"

urlpatterns = [
    # main
    path('', views.index, name="index"),

    # post
    path('posts', views.PostsView.as_view(), name="posts"),
    path('post/<pk>', views.post_detail, name="post_details"),
    path('post/<pk>/comment', views.post_comment, name="post_comment"),
    path('create/', views.post_create, name="post_create"),
    path('search/', views.post_search, name="post_search"),

    # path('login/', views.user_login, name="user_login"),
    path('login/', views.LoginView.as_view(), name="login"),

    path('loggedout/', auth_views.LogoutView.as_view(), name="logout"),
    path('logout/', views.logout_view, name="logout_confirm"),

    # other
    path('ticket/', views.ticket, name="ticket"),

    # user
    # path('<str:username>/', views.profile, name="profile"),

    path('<str:username>', views.profile, name="profile"),

    ]