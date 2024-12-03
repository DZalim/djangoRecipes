from django.contrib import admin

from djangoRecipes.common.models import Comment, Like


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["description", "comment_info"]
    search_fields = ["to_recipe__recipe_name",]
    list_filter = ["created_at", "user"]
    fieldsets = (
        ("Comment", {
            "fields": ("description",)
        }),
        ("Related Info", {
            "fields": ("to_recipe", "user",)
        }),
    )

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["like_info"]
    search_fields = ["to_recipe__recipe_name",]
    list_filter = ["user"]
    fieldsets = (
        ("Related Info", {
            "fields": ("to_recipe", "user",)
        }),
    )
