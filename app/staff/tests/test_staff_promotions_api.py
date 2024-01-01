"""Test Staff Promotion API"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from staff import models, serializers
from core.models import School
from core.tests import fake


def create_school():
    """create and return sample school"""
    defaults = fake.get_school_default_values()
    return School.objects.create(**defaults)


def create_staff(school):
    """Create and return sample staff member"""
    defaults = fake.get_staff_detail_default_values()
    return models.Staff.objects.create(
        school=school,
        **defaults
    )


def get_staff_promotion_url(staff_id):
    """Return a url for specific staff"""
    return reverse('staff:staff-promotions', args=[staff_id])


def get_staff_promotion_detail_urls(staff_id, pid):
    """Return the url for promotion details"""
    return reverse(
        'staff:staff-promotion_detail', args=[staff_id, pid]
    )


class PublicPromotionTests(TestCase):
    """Test unauthenticated API Request"""
    def setup(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required"""
        url = get_staff_promotion_url(staff_id=1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePromotionAPITest(TestCase):
    """Test Authenticated API Client"""
    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(
            **fake.get_school_default_values()
        )
        self.staff = models.Staff.objects.create(
            school=self.school,
            **fake.get_staff_detail_default_values()
        )
        self.user = get_user_model()\
            .objects.create_staff_account(
                account_id=self.staff.id,
                password='testpass@1234'
            )
        self.staff.account = self.user
        self.client.force_authenticate(user=self.staff.account)

    def test_staff_promotion_list(self):
        """Test staff user listing of promotions"""
        promo1 = models.Promotion.objects.create(
            **fake.get_promotion_default_values()
        )
        promo2 = models.Promotion.objects.create(
            **fake.get_promotion_default_values()
        )
        self.staff.promotions.add(promo1, promo2)
        self.staff.save()

        url = get_staff_promotion_url(staff_id=self.staff.id)
        res = self.client.get(url)
        promo1_data = serializers.PromotionSerializer(promo1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertIn(promo1_data.data, res.data)

    def test_staff_create_promotion(self):
        """Test that staff user create promotion success"""
        data = fake.get_promotion_default_values()

        url = get_staff_promotion_url(staff_id=self.staff.id)
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(data['rank'], res.data['rank'])

    def test_retrieve_specific_promo_for_staff(self):
        """Test retrieve a specific promotion for a staff user"""
        models.Promotion.objects.create(
            **fake.get_promotion_default_values()
        )
        promo = models.Promotion.objects.create(
            **fake.get_promotion_default_values(),
        )
        self.staff.promotions.add(promo)
        url = get_staff_promotion_detail_urls(
            staff_id=self.staff.id,
            pid=promo.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['rank'], promo.rank)

    def test_update_staff_promotion(self):
        """Test update staff promotion"""
        promotion = models.Promotion.objects.create(
            **fake.get_promotion_default_values()
        )
        self.staff.promotions.add(promotion)

        url = get_staff_promotion_detail_urls(
            staff_id=self.staff.id,
            pid=promotion.id
        )
        res = self.client.patch(url, {
            'rank': 'Updated rank'
        })
        promotion.refresh_from_db()

        self.assertEqual(res.data['rank'], 'Updated rank')
