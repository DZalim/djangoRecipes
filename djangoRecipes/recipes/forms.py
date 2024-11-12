from django import forms

from djangoRecipes.common.mixins import PlaceholderMixin, LabelMixin
from djangoRecipes.recipes.models import Recipe


class BaseRecipeForm(LabelMixin, forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_labels(show_labels=True)
