from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author_name', 'comment_text')
        labels = {
            'comment_text': '', 'author_name': ''
        }
        widgets = {
            'comment_text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Write your comment here...'
                }
            ),
            'author_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Write your name...'
                }
            ),
        }
