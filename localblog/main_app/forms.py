from django import forms
from .models import Comment, Post
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Write your comment here...', 'rows': 4}),
        }

class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of your post'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write your post here...', 'rows': 10}),
        }
