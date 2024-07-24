from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    description = models.TextField(max_length=800)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):

        return reverse('post-detail', kwargs={'post_id': self.id})

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'