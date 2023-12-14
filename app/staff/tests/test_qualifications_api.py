from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import School
from staff import models
from core.tests import fake

from rest_framework import status
from rest_framework.test import APIClient


def staff_qualification_url(staff_id):
    """Return a url for specific staff"""
    return reverse('staff:staff-qualifications', args=[staff_id])


def staff_qualification_detail_urls(staff_id, qid):
    """Return the url for qualification details"""
    return reverse(
        'staff:staff-qualification_detail',
        args=[staff_id, qid]
    )


def create_school():
    """create and return sample school"""
    defaults = fake.get_school_default_values()
    return School.objects.create(**defaults)


def create_staff(school):
    """Create and return sample staff member"""
    defaults = fake.get_staff_deteil_default_values()
    return models.Staff.objects.create(
        school=school,
        **defaults
    )


class PublicQualificationTests(TestCase):
    """Test unauthenticated API Request"""
    def setup(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required"""
        url = staff_qualification_url(staff_id=1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateQualificationAPITest(TestCase):
    """Test Authenticated API Client"""
    def setUp(self):
        self.admin_client = APIClient()
        self.staff_client = APIClient()
        self.school = create_school()
        self.staff = create_staff(school=self.school)
        self.admin_staff = create_staff(school=self.school)
        self.admin_staff.account = get_user_model()\
            .objects.create_admin_account(
            email='admin@example.com',
            password='secretpass@123'
        )
        self.staff.account = get_user_model().objects.create_staff_account(
            email='staff@example.com',
            password='superpass@123'
        )
        self.admin_client.force_authenticate(user=self.admin_staff.account)
        self.staff_client.force_authenticate(user=self.staff.account)

    def test_qualifications_limited_user(self):
        """Test that qualifications are limited to authenticated user"""
        qualification = models.Qualification.objects.create(
            staff=self.staff,
            **fake.get_qualification_default_values()
        )
        models.Qualification.objects.create(
            staff=self.admin_staff,
            **fake.get_qualification_default_values()
        )

        url = staff_qualification_url(staff_id=self.staff.id)
        res = self.admin_client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], qualification.title)
        self.assertEqual(res.data[0]['id'], qualification.id)

    def test_staff_create_qualification_success(self):
        """Test creating qualification for specfic staff successful"""

        data = fake.get_qualification_default_values()

        url = staff_qualification_url(staff_id=self.staff.id)
        res = self.staff_client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get('title'), data['title'])

    def test_update_staff_qualification_success(self):
        """Test update qualification for specific staff"""
        data = fake.get_qualification_default_values()
        qualification = models.Qualification.objects.create(
            staff=self.staff,
            **data
        )

        url = staff_qualification_detail_urls(
            staff_id=self.staff.id,
            qid=qualification.id
        )

        res = self.staff_client.patch(url, {'title': 'BSc. InfoTech'})
        qualification.refresh_from_db()
        self.assertEqual(res.data['title'], qualification.title)

    def test_retrieve_specific_qualification(self):
        """Test retriving a specif qualification object"""
        data = fake.get_qualification_default_values()
        qualification = models.Qualification.objects.create(
            staff=self.staff,
            **data
        )

        url = staff_qualification_detail_urls(
            staff_id=self.staff.id,
            qid=qualification.id
        )
        res = self.staff_client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], qualification.title)
