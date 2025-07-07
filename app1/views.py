import datetime

from django.contrib.auth.models import User
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Ticket
from .forms import TicketForm, PostCreateForm


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


class PostsView(ListView):
    queryset = Post.published.all()
    template_name = 'app1/posts.html'


def PostCreate(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Post.objects.create(
                auther=cd['auth'],
                title=cd['title'],
                publish=cd['publish'],
                image=cd['image'],
                description=cd['description'],
            )
            return redirect('app1:posts')
    else:
        form = PostCreateForm()
    return render(request, "forms/post_create.html", {'form':form})



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


# rezadolaty way to make a form :
# def ticket(request):
#     if request.method == "POST":
#         form = TicketForm(request.POST)
#         if form.is_valid():
#             ticket_obj = Ticket.objects.create()
#             cd = form.cleaned_data
#             ticket_obj.name = cd['name']
#             ticket_obj.message = cd['message']
#             ticket_obj.email = cd['email']
#             ticket_obj.phone = cd['phone']
#             ticket_obj.subject = cd['subject']
#             ticket_obj.publish = cd['publish']
#             ticket_obj.save()
#             return redirect("app1:ticket")
#     else:
#         form = TicketForm()
#     return render(request, 'forms/ticket.html', {'form': form})



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
                publish=cd['publish'],
            )
            return redirect("app1:ticket")
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})

