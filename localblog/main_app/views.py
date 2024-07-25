from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Like
from .forms import CommentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')


def post_index(request):
    user_posts = Post.objects.filter(author=request.user.username)
    other_posts = Post.objects.exclude(author=request.user.username)
    return render(request, 'posts/index.html', {'user_posts': user_posts, 'other_posts': other_posts})

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
    fields = ['title', 'description']
    success_url = '/posts'

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.author = self.request.user.username  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'author']

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/posts/'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('post-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )

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