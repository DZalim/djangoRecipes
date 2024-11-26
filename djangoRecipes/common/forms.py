from django import forms

from djangoRecipes.common.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']

        widgets = {
            'description': forms.Textarea(
                attrs={'placeholder': 'Add your comment....'}
            )
        }

class SearchForm(forms.Form):
    search_criteria = forms.CharField(required=False)
