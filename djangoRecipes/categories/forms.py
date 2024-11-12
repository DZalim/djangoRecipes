from django import forms

from djangoRecipes.categories.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ["user"]
