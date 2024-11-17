from django import forms

from djangoRecipes.photos.models import RecipePhotos, UsersPhoto


class AddRecipePhotoForm(forms.ModelForm):
    class Meta:
        model = RecipePhotos
        fields = ['photo_url']


class AddUserPhotoForm(forms.ModelForm):
    class Meta:
        model = UsersPhoto
        fields = ['photo_url']
