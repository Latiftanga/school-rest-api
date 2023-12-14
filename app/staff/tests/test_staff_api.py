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


from faker import Faker
from faker.providers import DynamicProvider


gender_provider = DynamicProvider(
    provider_name="gender",
    elements=['M', 'F'],
)


staff_category_provider = DynamicProvider(
    provider_name="staff_category",
    elements=['Teaching', 'Non Teaching'],
)


region_provider = DynamicProvider(
     provider_name="region",
     elements=[
        'Upper West', 'Upper East', 'North East',
        'Northern', 'Savanna', 'Bono East', 'Ahafo',
        'Western', 'Western North', 'Greater Accra',
        'Central', 'Volta', 'Oti'
     ],
)

fake = Faker()

fake.add_provider(gender_provider)
fake.add_provider(region_provider)
fake.add_provider(staff_category_provider)


STAFF_URL = reverse('staff:staff-list')


def staff_detail_url(staff_id):
    """Return a url for specific staff"""
    return reverse('staff:staff-detail', args=[staff_id])


def get_school_default_values():
    """Return some random values for the school object"""
    return {
        'name': fake.name(),
        'subdomain': fake.name(),
        'address': fake.address(),
        'city': fake.city(),
        'region': fake.state(),
        'phone': fake.phone_number(),
        'email': fake.email()
    }


def create_school(**params):
    """Create and return a sample school object"""
    defaults = get_school_default_values()
    defaults.update(params)
    return School.objects.create(**defaults)


def get_staff_deteil_default_values():
    """Return some random values for staff object"""
    return {
        'category': fake.staff_category(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'other_names': fake.first_name(),
        'gender': fake.gender(),
        'date_of_birth': fake.date(),
        'place_of_birth': fake.city(),
        'home_town': fake.city(),
        'home_region': fake.region(),
        'home_district': fake.city(),
        'nationality': fake.country(),
        'phone': fake.phone_number(),
        'residential_address': fake.address()
    }


def create_staff(school, **params):
    """Create and return a sample staff object"""
    defaults = get_staff_deteil_default_values()
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
        self.user = get_user_model().objects.create_admin_account(
            'admin@example.com',
            'password@123'
        )
        self.staff.account = self.user
        self.client.force_authenticate(self.staff.account)

    def test_retrieve_staff_list(self):
        """Test retrieving a list of staff"""
        create_staff(school=self.staff.school)
        create_staff(school=self.staff.school)
        create_staff(create_school())

        res = self.client.get(STAFF_URL)

        staff_list = models.Staff.objects.filter(
            school=self.user.staff.school
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
        payload = get_staff_deteil_default_values()
        payload['school'] = self.staff.school.id
        res = self.client.post(STAFF_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        staff = models.Staff.objects.get(id=res.data['id'])
        # for k, v in payload.items():
        #     self.assertEqual(getattr(staff, k), v)
        self.assertEqual(staff.school, self.user.staff.school)
