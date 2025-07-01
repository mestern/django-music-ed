import datetime
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from . models import Post


def index(request):
    return HttpResponse("index")


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts,
        'get_absolut_url': Post.get_absolute_url,
    }
    return render(request, "app1/list.html", context)


class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    paginate_by = 3
    template_name = 'app1/listp.html'



# def post_listp(request):
#
#     # give every posts with published status to posts to posts
#     posts = Post.published.all()
#
#     # give all of objects to paginator to be paginated
#     paginator = Paginator(posts, 3)
#
#     # get the page number from request
#     page_number = request.GET.get('page', 3)
#
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         # handle if page number is not exist
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         # handle if page's number is not an integer
#         posts = paginator.page(1)
#
#
#     context = {
#         'posts': posts,
#         'get_absolut_url': Post.get_absolute_url,
#         'page_number': page_number
#     }
#     return render(request, "app1/listp.html", context)


# def post_detail(request, id):
#     # dota rah dare yekish try except
#     # try:
#     #     post = Post.published.get(id=id)
#     # except:
#     #     raise Http404("page not found!")
#     # yekish get or 404
#     post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
#
#     context = {
#         'post': post,
#         'date': post.publish
#
#     }
#     return render(request, "app1/details.html", context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'app1/details.html'


