from django.template.defaulttags import url
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Ticket
from .forms import TicketForm, PostCreateForm, CommentFrom, SearchForm


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
    extra_context = {'get_absolut_url': Post.get_absolute_url}


def PostCreate(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd['auth'])
            Post.objects.create(
                auther = User.objects.get(username=cd['auth']),
                title=cd['title'],
                created=timezone.now(),
                image=cd['image'],
                description=cd['description'],
            )
            return redirect('app1:posts')
    else:
        form = PostCreateForm()
    return render(request, "forms/post_create.html", {'form':form})



# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'app1/details.html'


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentFrom()
    context = {
        'post': post,
        'comments': comments,
        'form': form
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
                publish=cd['publish'],
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