from django.urls import reverse
from rest_framework import status

from djangoRecipes.categories.models import Category
from tests.categories.category_setup import CategorySetUp


class TestEditDeleteCategoryView(CategorySetUp):

    def existing_category(self):
        existing_category = self.create_category(self.staff_user, "Test Category")
        category_url = reverse("edit-delete-category", kwargs={"pk": existing_category.pk})
        self.client.logout()

        return existing_category, category_url

    def access_denied(self, category_url):
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(category_url, {'category_name': 'Updated Category'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(category_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def allowed_access(self, category_url, existing_category):
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(category_url, {'category_name': 'Updated Category'}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_category.refresh_from_db()
        self.assertEqual(existing_category.category_name, 'Updated Category')

        response = self.client.delete(category_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Category.objects.filter(pk=existing_category.pk).exists())

    def test_unauthenticated_user_cannot_access(self):
        existing_category, category_url = self.existing_category()
        self.access_denied(category_url)

    def test_non_staff_user_cannot_edit_or_delete(self):
        existing_category, category_url = self.existing_category()
        user = self.regular_user
        self.client.login(username=user.username, password='password')

        self.access_denied(category_url)

    def test_staff_user_can_edit_and_delete_category(self):
        existing_category, category_url = self.existing_category()
        user = self.staff_user
        self.client.login(username=user.username, password='password')
        self.allowed_access(category_url, existing_category)

    def test_superuser_can_edit_and_delete_category(self):
        existing_category, category_url = self.existing_category()
        user = self.superuser
        self.client.login(username=user.username, password='password')
        self.allowed_access(category_url, existing_category)
