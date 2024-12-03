from django.contrib import admin

from djangoRecipes.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category_name", "created_at", "user",]
    search_fields = ["category_name", "created_at"]
    list_filter = ["category_name", "created_at", "user"]
    fieldsets = (
        ("Category Info", {
            "fields": ("category_name",)
        }),
        ("User Info", {
            "fields": ("user",)
        }),
    )
