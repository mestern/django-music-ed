import time

from Demos.win32ts_logoff_disconnected import username
from django.template.defaulttags import url
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages

from .models import Post, Ticket
from .forms import *
from django.contrib.auth import authenticate, login, logout


def index(request):
    return HttpResponse("آروم بگیر مرد")


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


class PostsView(ListView):
    queryset = Post.published.all()
    template_name = 'app1/posts.html'
    extra_context = {'get_absolut_url': Post.get_absolute_url,
                     'images': Post.get_images,
                     }


def PostCreate(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if not request.user.is_anonymous:
            if form.is_valid():
                post = form.save(commit=False)
                post.auther = request.user
                post.save()
                Image.objects.create(image=form.cleaned_data['image'], post=post, title=post.title)
                return redirect('app1:posts')
        else:
            return HttpResponse("login to your account first")
    else:
        form = PostCreateForm()
    return render(request, "forms/post_create.html", {'form': form})


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'app1/details.html'


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    images = post.image.all()
    form = CommentFrom()
    context = {
        'post': post,
        'comments': comments,
        'images': images,
        'form': form,
    }


    return render(request, 'app1/details.html', context)


# chatgpt way to make a form view:

def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assume you're getting a valid user object her

            Ticket.objects.create(
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject'],
                message=cd['message'],
            )
            return redirect("app1:ticket")
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentFrom(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect("app1:post_details", pk)
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comment.html', context)


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.filter(title__icontains=query)
    context = {
        'query': query,
        'object_list': results,
    }
    print(results)
    return render(request, 'app1/posts.html', context)


# @require_POST
# def post_image(request, pk):
#     post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
#     image = None
#     form = ImageForm(request.post)
#     if form.is_valid():
#         image = form.save(commit=False)
#         image.post = post


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "Login Successful")
                    return redirect("app1:posts")
                else:
                    messages.add_message(request, messages.ERROR, "The account is inactive.")

            else:
                messages.error(request, "Username or Password is Incorrect")
    else:
        form = LoginForm()

    context = {
        "form": form
    }
    return render(request, "forms/login_form.html", context)