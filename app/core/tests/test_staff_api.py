from django.test import TestCase
# from django.urls import reverse
from django.contrib.auth import get_user_model

# from rest_framework import status
from rest_framework.test import APIClient

from core.models import School
from core.tests import fake
from staff import models


class TestStaffPrivateAPITest(TestCase):
    """Test private API for Staff User"""
    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(
            **fake.get_school_default_values()
        )
        self.staff = models.Staff.objects.create(
            school=self.school,
            **fake.get_staff_deteil_default_values()
        )
        self.staff.account = self.user
        self.user = get_user_model()\
            .objects.create_staff_account(
                email='teacher@example.com',
                password='testpass@1234'
            )
        self.client.force_authenticate(user=self.staff.account)
