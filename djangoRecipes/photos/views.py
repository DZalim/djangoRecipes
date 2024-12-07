from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from djangoRecipes.common.permissions import SameUserPermissions
from djangoRecipes.photos.forms import AddRecipePhotoForm, AddUserPhotoForm
from djangoRecipes.photos.models import RecipePhotos, UsersPhoto
from djangoRecipes.recipes.models import Recipe

UserModel = get_user_model()


class AddRecipePhotoView(SameUserPermissions, CreateView):
    model = RecipePhotos
    form_class = AddRecipePhotoForm
    template_name = "photos/add-photo-view.html"

    def get_object(self, queryset=None):
        recipe_id = self.kwargs["pk"]
        return get_object_or_404(Recipe, pk=recipe_id)

    def form_valid(self, form):
        recipe_id = self.kwargs["pk"]
        recipe = Recipe.objects.get(pk=recipe_id)

        photo = form.save(commit=False)
        photo.recipe = recipe
        photo.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe-details', kwargs={'pk': self.kwargs['pk']})


class DeleteRecipePhotoView(SameUserPermissions, DeleteView):
    model = RecipePhotos

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['photo_pk'])

    def get_success_url(self):
        return reverse_lazy('recipe-details', kwargs={'pk': self.kwargs['pk']})


class AddUserPhotoView(SameUserPermissions, CreateView):
    model = UsersPhoto
    form_class = AddUserPhotoForm
    template_name = "photos/add-photo-view.html"

    def get_object(self, queryset=None):
        user_id = self.kwargs["pk"]
        return get_object_or_404(UserModel, pk=user_id)

    def form_valid(self, form):
        user_id = self.kwargs["pk"]
        user = UserModel.objects.get(pk=user_id)

        photo = form.save(commit=False)
        photo.user = user
        photo.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.kwargs['pk']})


class ChangeUserPhotoView(SameUserPermissions, UpdateView):
    model = UsersPhoto
    form_class = AddUserPhotoForm
    template_name = "photos/change-photo-view.html"

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['photo_pk'])

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.delete_photo_from_cloudinary()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.kwargs['pk']})


class DeleteUserPhotoView(SameUserPermissions, DeleteView):
    model = UsersPhoto

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['photo_pk'])

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.kwargs['pk']})
