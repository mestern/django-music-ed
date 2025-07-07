from django.urls import path
from . import views

app_name = "app1"

urlpatterns = [

    path('', views.index, name="index"),
    path('postli', views.post_list, name="post_list"),
    path('postp', views.PostListView.as_view(), name="post_listp"),
    path('post/<pk>', views.PostDetailView.as_view(), name="post_details"),
    path('ticket', views.ticket, name="ticket"),
    path('posts', views.PostsView.as_view(), name="posts")

    # path('post/<int:id>', views.post_detail, name="post_details"),
    # path('postp/', views.post_listp, name="post_listp"),

]