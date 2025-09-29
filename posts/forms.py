# forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # NEW: for replies

    class Meta:
        model = Comment
        fields = ['content']  # keep only content in the visible form
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'})
        }
