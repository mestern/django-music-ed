import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from . models import Post


def index(request):
    return HttpResponse("index")


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts,
        'get_absolut_url': Post.get_absolute_url
    }
    return render(request, "app1/list.html", context)


def post_detail(request, id):
    # dota rah dare yekish try except
    # try:
    #     post = Post.published.get(id=id)
    # except:
    #     raise Http404("page not found!")
    # yekish get or 404
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    context = {
        'post': post,
        'date': post.publish

    }
    return render(request, "app1/details.html", context)
