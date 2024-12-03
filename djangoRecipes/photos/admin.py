from django.contrib import admin

from djangoRecipes.photos.models import RecipePhotos, UsersPhoto


@admin.register(RecipePhotos)
class RecipePhotosAdmin(admin.ModelAdmin):
    list_display = ["photo_url", "created_at", "recipe"]
    search_fields = ["recipe__recipe_name",]
    list_filter = ["created_at"]
    fieldsets = (
        ("Photo", {
            "fields": ("photo_url",)
        }),
        ("Related Info", {
            "fields": ("recipe",)
        }),
    )

@admin.register(UsersPhoto)
class UsersPhotoAdmin(admin.ModelAdmin):
    list_display = ["photo_url", "created_at", "user"]
    list_filter = ["created_at", "user"]
    fieldsets = (
        ("Photo", {
            "fields": ("photo_url",)
        }),
        ("Related Info", {
            "fields": ("user",)
        }),
    )
