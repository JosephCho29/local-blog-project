from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Like
from .forms import CommentForm, PostForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def post_index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

@login_required
def our_archive(request):
    user_posts = Post.objects.filter(author=request.user.username)
    return render(request, 'posts/our_archive.html', {'posts': user_posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'posts/detail.html', {'post': post, 'comments': comments, 'form': form})

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = '/posts'

    def form_valid(self, form):
        form.instance.author = self.request.user.username
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/posts/'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        liked.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'likes': post.total_likes, 'liked': liked})
