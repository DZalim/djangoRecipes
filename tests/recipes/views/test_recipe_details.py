from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from djangoRecipes.categories.models import Category
from djangoRecipes.recipes.models import Recipe

UserModel = get_user_model()


class TestRecipeDetailsView(TestCase):
    def setUp(self):
        # Create users
        self.regular_user = UserModel.objects.create_user(email="regular@mail.bg", username='regular', password='password')
        self.staff_user = UserModel.objects.create_user(email="staff@mail.bg", username='staff', password='password', is_staff=True)
        self.super_user = UserModel.objects.create_user(email="super@mail.bg", username='super', password='password', is_superuser=True)
        self.other_regular_user = UserModel.objects.create_user(email="other_regular@mail.bg", username='other_regular', password='password')

        # Create category
        self.category = Category.objects.create(
            category_name="Category Name",
            user=self.staff_user
        )

        # Create recipes
        self.approved_recipe = Recipe.objects.create(
            recipe_name="Approved Recipe",
            difficulty_level="easy",
            portions=3,
            preparing_time=10,
            cooking_time=15,
            ingredients="Sugar;Flour;Milk",
            description="aa" * 50,
            is_approved=True,
            category=self.category,
            user=self.regular_user,
        )
        self.unapproved_recipe = Recipe.objects.create(
            recipe_name="Unapproved Recipe",
            difficulty_level="easy",
            portions=3,
            preparing_time=10,
            cooking_time=15,
            ingredients="Eggs;Butter",
            description="bb" * 50,
            is_approved=False,
            category=self.category,
            user=self.regular_user,
        )

    def test_anonymous_user_access_unapproved_recipe(self):
        response = self.client.get(reverse('recipe-details', kwargs={'pk': self.unapproved_recipe.pk}))
        self.assertEqual(response.status_code, 404)

    def test_regular_user_access_unapproved_recipe(self):
        self.client.login(username='other_regular', password='password')
        response = self.client.get(reverse('recipe-details', kwargs={'pk': self.unapproved_recipe.pk}))
        self.assertEqual(response.status_code, 404)

    def test_owner_access_unapproved_recipe(self):
        self.client.login(username='regular', password='password')
        response = self.client.get(reverse('recipe-details', kwargs={'pk': self.unapproved_recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unapproved Recipe")

    def test_staff_user_access_unapproved_recipe(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('recipe-details', kwargs={'pk': self.unapproved_recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unapproved Recipe")

    def test_superuser_access_unapproved_recipe(self):
        self.client.login(username='super', password='password')
        response = self.client.get(reverse('recipe-details', kwargs={'pk': self.unapproved_recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unapproved Recipe")

    def test_access_approved_recipe(self):
        # Anonymous user
        response = self.client.get(reverse('recipe-details', kwargs={'pk': self.approved_recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Recipe")

        # Logged-in user
        self.client.login(username='other_regular', password='password')
        response = self.client.get(reverse('recipe-details', kwargs={'pk': self.approved_recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Recipe")
