from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from djangoRecipes.common.forms import CommentForm
from djangoRecipes.common.models import Like
from djangoRecipes.recipes.models import Recipe


def home_view(request):
    return render(request, 'common/home-view.html')

@login_required
def like_functionality(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    liked_object = Like.objects.filter(to_recipe=recipe_id, user=request.user).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_recipe=recipe, user=request.user)
        like.save()

    return redirect(reverse('recipe-details', kwargs={'pk': recipe.id}))

@login_required
def comment_functionality(request, recipe_id):
    if request.POST:
        recipe = Recipe.objects.get(id=recipe_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_recipe = recipe
            comment.user = request.user
            comment.save()

            response_data = {
                'user': comment.user.profile.get_full_name(),
                'description': comment.description,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
            }

            return JsonResponse(response_data, status=201)

        return JsonResponse({'error': 'Invalid form data'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
