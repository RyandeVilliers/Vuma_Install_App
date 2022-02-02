from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='ryantest@vumatel.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "ryandv62@gmail.com"
        password = "TestPass123"
        # calling create user function on the user manager for our user model
        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email, email)

        # returns true if password is correct, false if not correct

        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """Test the email for a new user us normalised"""
        email = 'test@VUMATEL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating email with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@vumatel.com',
            'test123'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_status_str(self):
        """Test the status string representation"""
        status_check = models.Status.objects.create(
            user=sample_user(),
            status='Installation Requested'
        )
        self.assertEqual(str(status_check), status_check.status)

    def test_installation_str(self):
        """Test the recipe string representation"""
        installation = models.Installation.objects.create(
            user=sample_user(),
            customer_name='Phillip Moss',
            address='17 Petunia Street',

        )
        self.assertEqual(str(installation), installation.customer_name)
