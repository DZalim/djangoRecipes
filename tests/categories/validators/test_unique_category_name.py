from djangoRecipes.categories.models import Category
from tests.categories.category_setup import CategorySetUp


class TestCategoryUniqueName(CategorySetUp):

    def create_other_category(self, user, name):
        """Helper method to create a other category with same name."""
        self.client.login(username=user.username, password='password')

        response = self.client.get(self.add_category_url)
        self.assertEqual(response.status_code, 200)

        post_response = self.client.post(self.add_category_url, {'category_name': name})

        return post_response

    def assert_category_creation_fails_due_to_duplicate(self, user, category_name):
        """Helper method to assert category creation fails due to duplicate name."""
        self.create_category(user, category_name)

        post_response = self.create_other_category(user, category_name)
        self.assertEqual(post_response.status_code, 200)

        form = post_response.context['form']
        self.assertTrue(form.errors.get('category_name'))
        self.assertIn('Тhis category already exists!', form.errors['category_name'])

        self.assertEqual(Category.objects.filter(category_name=category_name).count(), 1)

    def test_create_category_with_duplicate_name_by_staff_user(self):
        self.assert_category_creation_fails_due_to_duplicate(self.staff_user, 'Test Category')

    def test_create_category_with_duplicate_name_by_superuser(self):
        self.assert_category_creation_fails_due_to_duplicate(self.superuser, 'Test Category')
