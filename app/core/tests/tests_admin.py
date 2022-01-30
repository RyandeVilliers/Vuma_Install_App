from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse  # allows us to generate urls from admin page


class AdminSiteTests(TestCase):

    # Set Up
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@vumatel.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@vumatel.com',
            password='password123',
            name='Test User Full Name'
        )

    def test_for_users_listed(self):
        """Test that users are listed on user page"""
        # Dynamically updates, instead of hardcoding
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
