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

        right_column_fields = ["ingredients", "description"]

        for field_name, field in self.fields.items():
            if field_name in right_column_fields:
                field.widget.attrs.update({'class': 'form-column-right'})
            else:
                field.widget.attrs.update({'class': 'form-column-left'})
