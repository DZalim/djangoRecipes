from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class TestEditProfile(TestCase):

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

        self.edit_profile = reverse('edit-profile', kwargs={'pk': self.regular_user.pk})

    def test_edit_profile__access_anonymous_user(self):
        response = self.client.get(self.edit_profile)
        self.assertEqual(response.status_code, 403)

    def test_edit_profile__access_same_user_and_update(self):
        user = self.regular_user
        self.client.login(username=user.username, password='password')
        response = self.client.get(self.edit_profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/update-profile-form.html')

        post_response = self.client.post(self.edit_profile, {
            "username": user.username,
            "email": user.email,
            'first_name': 'First Name'
        })

        user.profile.refresh_from_db()
        self.assertEqual(user.profile.first_name, 'First Name')

        self.assertRedirects(post_response, reverse('profile-details', kwargs={'pk': user.pk}))

    def test_edit_profile__access_different_user(self):
        user = self.other_regular
        self.client.login(username=user.username, password='password')
        response = self.client.get(self.edit_profile)
        self.assertEqual(response.status_code, 403)
