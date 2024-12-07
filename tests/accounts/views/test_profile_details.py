from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class TestProfileDetails(TestCase):

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

        self.other_regular = UserModel.objects.create_user(
            email="other_regular@mail.bg",
            username='other_regular',
            password='password',
            is_superuser=True
        )

        self.profile_details = reverse('profile-details', kwargs={'pk': self.regular_user.pk})

    def test_access_anonymous_user(self):
        response = self.client.get(self.profile_details)
        self.assertEqual(response.status_code, 403)

    def test_access_same_user(self):
        user = self.regular_user
        self.client.login(username=user.username, password='password')
        response = self.client.get(self.profile_details)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Hello, {user.username}")

    def test_access_different_user(self):
        user = self.other_regular
        self.client.login(username=user.username, password='password')
        response = self.client.get(self.profile_details)
        self.assertEqual(response.status_code, 403)

    def test_access_invalid_user(self):
        user = self.other_regular
        self.client.login(username=user.username, password='password')
        response = self.client.get(reverse('profile-details', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 403)

    def test_access_by_staff(self):
        user = self.staff_user
        self.client.login(username=user.username, password='password')
        response = self.client.get(self.profile_details)
        self.assertEqual(response.status_code, 403)

    def test_access_by_superuser(self):
        user = self.superuser
        self.client.login(username=user.username, password='password')
        response = self.client.get(self.profile_details)
        self.assertEqual(response.status_code, 403)