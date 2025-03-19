from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author_name', 'comment_text')
        widgets = {'body': forms.Textarea(attrs={'class': 'form-control'})}
