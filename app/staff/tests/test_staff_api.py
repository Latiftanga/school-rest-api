"""Test for staff APIs"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from staff import models
from core.models import School
from staff.serializers import (
    StaffSerializer,
    StaffDetailSerializer
)
from core.tests import fake


STAFF_URL = reverse('staff:staff-list')


def staff_detail_url(staff_id):
    """Return a url for specific staff"""
    return reverse('staff:staff-detail', args=[staff_id])


def create_school(**params):
    """Create and return a sample school object"""
    defaults = fake.get_school_default_values()
    defaults.update(params)
    return School.objects.create(**defaults)


def create_staff(school, **params):
    """Create and return a sample staff object"""
    defaults = fake.get_staff_detail_default_values()
    defaults.update(params)
    staff = models.Staff.objects.create(
        school=school,
        **defaults
    )
    return staff


class PrivateStaffAPITests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        school = create_school()
        self.staff = create_staff(school=school)
        self.staff.account = get_user_model().objects.create_admin_account(
            self.staff.id,
            'password@123'
        )
        self.client.force_authenticate(self.staff.account)

    def test_retrieve_staff_list(self):
        """Test retrieving a list of staff"""
        create_staff(school=self.staff.school)
        create_staff(school=self.staff.school)
        create_staff(create_school())

        res = self.client.get(STAFF_URL)

        staff_list = models.Staff.objects.filter(
            school=self.staff.school
        ).order_by('-first_name')

        serializer = StaffSerializer(staff_list, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_staff_detail(self):
        """Test get Staff detail"""
        staff = create_staff(
            school=self.staff.school
        )
        url = staff_detail_url(staff.id)

        res = self.client.get(url)

        serializer = StaffDetailSerializer(staff)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_staff(self):
        """Test Creating a Staff"""
        payload = fake.get_staff_detail_default_values()
        res = self.client.post(STAFF_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        staff = models.Staff.objects.get(id=res.data['id'])
        # for k, v in payload.items():
        #     self.assertEqual(getattr(staff, k), v)
        self.assertEqual(staff.school, self.staff.school)

    def test_create_staff_with_account(self):
        """Test creating a staff with user account sucess"""
        payload = fake.get_staff_detail_default_values()
        payload['school'] = self.staff.school.id
        payload['has_account'] = True
        payload['email'] = 'admin@example.com'
        res = self.client.post(STAFF_URL, payload)
        # print(res.data)
        staff = models.Staff.objects.get(id=res.data['id'])

        self.assertTrue(res.data['has_account'], True)
        self.assertEqual(staff.account.email, payload['email'])

    def test_create_staff_with_account_without_email(self):
        """Test that create staf without a valid email raise error"""
        payload = fake.get_staff_detail_default_values()
        payload.update({'school': self.staff.school.id, 'has_account': True})

        res = self.client.post(STAFF_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValueError)
