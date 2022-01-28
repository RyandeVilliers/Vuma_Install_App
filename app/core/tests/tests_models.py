from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "ryandv62@gmail.com"
        password = "TestPass123"
        # calling create user function on the user manager for our user model
        user = get_user_model().objects.create_user(
            email = email,
            password = password
            )

        self.assertEqual(user.email, email)

        # returns true if password is correct, false if not correct

        self.assertTrue(user.check_password(password))