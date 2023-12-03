"""
 Test user
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


TOKEN_URL = reverse('core:token')
ME_URL = reverse('core:me')


def create_user_account(**params):
    """create and return a sample user """
    return get_user_model().objects.create_user(
        **params
    )


class TestUserAPI(TestCase):
    """Test for user token generation"""

    def test_create_token_for_user_account(self):
        """Test generate token for valid credentials"""
        user_details = {
            'email': 'test@example.com',
            'password': 'password@1234'
        }
        create_user_account(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error if credentials invalid"""
        create_user_account(
            email='test@example.com',
            password='password@1234'
        )
        payload = {'email': 'pass@eg.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting blank password return error"""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Test API that require authentication"""
    def setUp(self):
        self.user = create_user_account(
            email='test@example.com',
            password='testpass@123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.data, {
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """POST not allowed for the me endpoint"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {
            'email': 'updatedmail@examle.com',
            'password': 'NewPass@123'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
