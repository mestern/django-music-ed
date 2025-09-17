from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *

#  ___________-------------main section-------------_____________
def index(request):
    return render(request, "app1/home.html")



#  ___________-------------posts section-------------_____________
class PostsView(ListView):
    queryset = Post.published.all()
    template_name = 'app1/posts.html'
    # extra_context = {'get_absolut_url': Post.get_absolute_url,}

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


def post_create(request):
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
    return render(request, 'app1/posts.html', context)


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


# @require_POST
# def post_image(request, pk):
#     post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
#     image = None
#     form = ImageForm(request.post)
#     if form.is_valid():
#         image = form.save(commit=False)
#         image.post = post


#  ___________-------------authentication section-------------_____________

# def user_login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     messages.add_message(request, messages.SUCCESS, "Login Successful")
#                     return redirect("app1:posts")
#                 else:
#                     messages.add_message(request, messages.ERROR, "The account is inactive.")
#
#             else:
#                 messages.error(request, "Username or Password is Incorrect")
#     else:
#         form = LoginForm()
#
#     context = {
#         "form": form
#     }
#     return render(request, "forms/login.html", context)\


class LoginView(LoginView):
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        username = self.request.user.get_username()
        return reverse('app1:profile', kwargs={'username': username})


@login_required()
def logout_view(request):
    return render(request, 'registration/logout_confirm.html')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    template = "app1/user_profile.html" if user == request.user else "app1/profile.html"
    posts = Post.published.filter(auther=user)
    return render(request, template, {"user": user, "posts": posts})