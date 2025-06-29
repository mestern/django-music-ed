from django.urls import path
from . import views

app_name = "app1"

urlpatterns = [

    path('', views.index, name="index"),
    path('posts', views.post_list, name="post_list"),
    path('post/<int:id>', views.post_detail, name="post_details"),
    path('postp/', views.post_listp, name="post_listp"),
]