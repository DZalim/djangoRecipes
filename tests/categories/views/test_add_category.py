from tests.categories.category_setup import CategorySetUp


class TestAddCategoryView(CategorySetUp):

    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.add_category_url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_cannot_access(self):
        self.client.login(username="regular", password="password")
        response = self.client.get(self.add_category_url)
        self.assertEqual(response.status_code, 403)

    def test_staff_user_can_access_and_create_category(self):
        self.create_category(self.staff_user, "Category Name")

    def test_superuser_can_access_and_create_category(self):
        self.create_category(self.superuser, "Category Name")
