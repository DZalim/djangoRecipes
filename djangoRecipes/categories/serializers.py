from rest_framework import serializers

from djangoRecipes.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]

    def validate_category_name(self, value):
        category_name_lower = value.lower()

        if Category.objects.filter(category_name__iexact=category_name_lower).exists():
            raise serializers.ValidationError("This category already exists!")

        return value
