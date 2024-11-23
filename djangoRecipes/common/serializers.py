from rest_framework import serializers

from djangoRecipes.common.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "description", "created_at"]
