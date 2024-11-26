from django import forms
from django.core.exceptions import ValidationError

from djangoRecipes.common.mixins import LabelMixin
from djangoRecipes.recipes.models import Recipe


class BaseRecipeForm(LabelMixin, forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ["user", "is_approved"]

        widgets = {
            'portions': forms.NumberInput(
                attrs={'placeholder': 'For how many people....'}
            ),
            'preparing_time': forms.NumberInput(
                attrs={'placeholder': 'Add the preparing time in minutes....'}
            ),
            'cooking_time': forms.NumberInput(
                attrs={'placeholder': 'Add the cooking time in minutes....'}
            ),
            'ingredients': forms.Textarea(
                attrs={'placeholder': 'Must be entered with a semicolon(;).\n'
                                      'For example: 1 pack spaghetti; 1 tbsp olive oil; 1 garlic clove halved; 77g pack pancetta; '
                                      '1 chicken breast cut into strips; 2 eggs; '
                                      '100g Grana Padano; finely grated, plus extra to serve ('
                                      'wrap the rest tightly and it will keep for several weeks); '
                                      '1 tbsp butter..'}
            ),
            'description': forms.Textarea(
                attrs={'placeholder': "Cook the spaghetti following pack instructions. "
                                      "Meanwhile, heat the oil in a frying pan and fry the garlic "
                                      "and pancetta until crisp, then add the chicken strips and fry "
                                      "briefly until they're just cooked through. "
                                      "Fish out the garlic clove and discard it. "
                                      "Beat the eggs with the grana padano and some black pepper."}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_labels(show_labels=True)

        right_column_fields = ["ingredients", "description"]

        for field_name, field in self.fields.items():
            if field_name in right_column_fields:
                field.widget.attrs.update({'class': 'form-column-right'})
            else:
                field.widget.attrs.update({'class': 'form-column-left'})


class CreateRecipeForm(BaseRecipeForm):
    pass


class EditRecipeForm(BaseRecipeForm):
    class Meta:
        model = Recipe
        exclude = ["user", "is_approved"]

    def clean_recipe_name(self):
        recipe_name = self.cleaned_data['recipe_name']
        instance = self.instance

        if Recipe.objects.filter(recipe_name=recipe_name).exclude(pk=instance.pk).exists():
            raise ValidationError("A recipe with the same name already exists. Please choose another name!")

        return recipe_name

