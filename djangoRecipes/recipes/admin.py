from django.contrib import admin

from djangoRecipes.recipes.models import Recipe


@admin.register(Recipe)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["recipe_name", "difficulty_level", "portions", "preparing_time", "cooking_time",
                    "category", "user"]
    search_fields = ["recipe_name", "difficulty_level", "portions", "preparing_time", "cooking_time"]
    list_filter = ["recipe_name", "difficulty_level", "portions", "preparing_time", "cooking_time",
                   "category", "user", "created_at"]
    fieldsets = (
        ("Recipe Info", {
            "fields": ("recipe_name", "difficulty_level", "portions", "preparing_time", "cooking_time",)
        }),
        ("How to Cook", {
            "fields": ("ingredients", "description",)
        }),
        ("Related Info", {
            "fields": ("category", "user",)
        }),
    )
