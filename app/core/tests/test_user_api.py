"""
 Test user
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import School

from staff import serializers
from staff import models
from core.tests import fake


TOKEN_URL = reverse('core:auth')
ME_URL = reverse('core:profile')


def create_user_account(**params):
    """create and return a sample user """
    return get_user_model().objects.create_user(
        **params
    )


def create_school(**params):
    """Create and return a sample school object"""
    defaults = {}
    defaults.update(params)
    return School.objects.create(**defaults)


def create_staff(school, **params):
    """Create and return a sample staff object"""
    defaults = fake.get_staff_deteil_default_values()
    defaults.update(params)
    staff = models.Staff.objects.create(
        school=school,
        **defaults
    )
    return staff


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
        self.admin_client = APIClient()
        self.staff_client = APIClient()
        self.admin_account = get_user_model().objects.create_admin_account(
            email='test@example.com',
            password='testpass@123'
        )
        self.staff_account = get_user_model().objects.create_staff_account(
            email='staff@example.com',
            password='testpass@123'
        )
        self.school = create_school(
            **fake.get_school_default_values()
        )
        self.admin_staff = create_staff(
            school=self.school,
            **fake.get_staff_deteil_default_values()
        )
        self.staff = create_staff(
            school=self.school,
            **fake.get_staff_deteil_default_values(),
        )
        self.staff.account = self.staff_account
        self.admin_staff.account = self.admin_account
        self.admin_client.force_authenticate(user=self.admin_staff.account)
        self.staff_client.force_authenticate(user=self.staff.account)

    def test_retrieve_admin_user_profile_success(self):
        """Test retrieving profile for logged in user"""

        res = self.admin_client.get(ME_URL)
        serializer = serializers.StaffDetailSerializer(self.admin_staff)
        self.assertEqual(res.data, {
            'email': self.admin_account.email,
            'profile': serializer.data
        })

    def test_retrieve_staff_user_profile_success(self):
        """Test retrieving login staff user profile success"""
        res = self.staff_client.get(ME_URL)

        serializer = serializers.StaffDetailSerializer(self.staff)

        self.assertEqual(
            res.data,
            {
                'email': self.staff_account.email,
                'profile': serializer.data

            }
        )

    def test_post_me_not_allowed(self):
        """POST not allowed for the me endpoint"""
        res = self.admin_client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {
            'email': 'updatedmail@examle.com',
            'password': 'NewPass@123'
        }
        res = self.admin_client.patch(ME_URL, payload)

        self.admin_account.refresh_from_db()
        self.assertTrue(self.admin_account.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
