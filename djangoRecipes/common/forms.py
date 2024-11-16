from django import forms

from djangoRecipes.common.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']

        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'Add your comment....'}
            )
        }
