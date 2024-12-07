from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from djangoRecipes.categories.models import Category

UserModel = get_user_model()


class CategorySetUp(TestCase):

    def setUp(self):
        self.regular_user = UserModel.objects.create_user(
            email="regular@mail.bg",
            username='regular',
            password='password'
        )

        self.staff_user = UserModel.objects.create_user(
            email="staff@mail.bg",
            username='staff',
            password='password',
            is_staff=True
        )
        self.superuser = UserModel.objects.create_user(
            email="super@mail.bg",
            username='super',
            password='password',
            is_superuser=True
        )

        self.add_category_url = reverse('add-category')

    def create_category(self, user, name):
        """Helper method to create a category."""
        self.client.login(username=user.username, password="password")

        response = self.client.get(self.add_category_url)
        self.assertEqual(response.status_code, 200)

        post_response = self.client.post(self.add_category_url, {'category_name': 'Test Category'})

        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse('list-categories'))

        created_category = Category.objects.filter(category_name='Test Category')
        self.assertTrue(created_category.exists())

        return created_category.first()
