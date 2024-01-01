"""
 Test models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models."""
    def test_create_user_with_ID_successful(self):
        """Test creating a suer with an ID is successful"""
        account_id = 'USER002'
        password = 'pass@123'
        user = get_user_model().objects.create_user(
            account_id=account_id,
            password=password
        )

        self.assertEqual(user.account_id, account_id)
        self.assertTrue(user.check_password(password))

    # def test_new_user_email_normalized(self):
    #     """Test email is normalized for new user creation"""
    #     sample_emails = [
    #         ['test1@EXAMPLE.com', 'test1@example.com'],
    #         ['Test2@Example.com', 'Test2@example.com'],
    #         ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
    #         ['test4@example.COM', 'test4@example.com'],
    #     ]

    #     for email, expected in sample_emails:
    #         user = get_user_model().objects.create_user(email, 'sample123')
    #         self.assertEqual(user.email, expected)

    def test_new_user_without_ID_raises_error(self):
        """Test that creating a user without an ID raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'SUPER03',
            'super@123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
