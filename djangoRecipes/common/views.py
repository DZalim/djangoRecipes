from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from djangoRecipes.common.models import Like, Comment
from djangoRecipes.common.permissions import IsSameUser
from djangoRecipes.common.serializers import CommentSerializer
from djangoRecipes.recipes.models import Recipe


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


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        recipe_id = self.kwargs['recipe_id']
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise serializers.ValidationError({'error': 'Recipe not found'})

        serializer.save(user=self.request.user, to_recipe=recipe)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response_data = response.data

        response_data['user'] = request.user.profile.get_full_name()

        return Response(response_data, status=status.HTTP_201_CREATED)


class CommentEditDeleteView(UpdateAPIView, DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsSameUser]

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, pk=comment_id)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()

        if request.user != comment.user:
            return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'description': serializer.data['description']})

        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
