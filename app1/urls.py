from django.urls import path
from . import views

app_name = "app1"

urlpatterns = [

    path('', views.index, name="index"),
    path('postli', views.post_list, name="post_list"),
    path('postp', views.PostListView.as_view(), name="post_listp"),
    path('post/<pk>', views.post_detail, name="post_details"),
    path('post/<pk>/comment', views.post_comment, name="post_comment"),
    path('ticket', views.ticket, name="ticket"),
    path('posts', views.PostsView.as_view(), name="posts"),
    path('create', views.PostCreate, name="post_create"),
    path('search/', views.post_search, name="post_search"),
    path('login/', views.user_login, name="user_login"),

    # path('post/<int:id>', views.post_detail, name="post_details"),
    # path('postp/', views.post_listp, name="post_listp"),

]