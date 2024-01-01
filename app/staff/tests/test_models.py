"""Test for models"""
from django.test import TestCase
from core.models import School
from staff import models
from core.tests import fake


class TestModels(TestCase):
    """Test models."""

    def test_create_staff(self):
        """test creating a staff is successful"""
        school = School.objects.create(
            **fake.get_school_default_values()
        )

        staff_details = fake.get_staff_detail_default_values()
        staff = models.Staff.objects.create(
            school=school,
            **staff_details,
        )
        self.assertEqual(
            staff.first_name,
            staff_details['first_name']
        )

    def test_create_promotion(self):
        """Test creating promotion for specific staff"""
        school = School.objects.create(
            **fake.get_school_default_values()
        )

        staff_details = fake.get_staff_detail_default_values()
        staff = models.Staff.objects.create(
            school=school,
            **staff_details,
        )
        promotion = models.Promotion.objects.create(
            staff=staff,
            **fake.get_promotion_default_values()
        )

        self.assertEqual(str(promotion), promotion.rank)

    def test_create_qualification(self):
        """Test creating qualification for specific staff"""
        school = School.objects.create(
            **fake.get_school_default_values()
        )

        staff_details = fake.get_staff_detail_default_values()
        staff = models.Staff.objects.create(
            school=school,
            **staff_details,
        )
        qualification = models.Qualification.objects.create(
            staff=staff,
            **fake.get_qualification_default_values()
        )

        self.assertEqual(str(qualification), qualification.title)
