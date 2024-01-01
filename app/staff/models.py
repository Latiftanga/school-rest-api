from django.db import models
from django.contrib.auth import get_user_model

from core.models import Person, School


class Staff(Person):
    """staff in the system"""
    STAFF_CATEGORIES = [
        ('Teaching', 'Teaching'),
        ('Non Teaching', 'Non Teaching'),
    ]

    @classmethod
    def generate_staff_id(cls):
        prefix = 'TR'
        seq_no = 1  # Starting sequence number
        while Staff.objects.filter(id=f"{prefix}{seq_no:08}").exists():
            seq_no += 1
        return f"{prefix}{seq_no:08}"

    category = models.CharField(
        max_length=128, choices=STAFF_CATEGORIES
    )
    id = models.CharField(
        max_length=255, unique=True, primary_key=True
    )
    registered_no = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    sssnit_no = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    license_no = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    date_appointed = models.DateField(blank=True, null=True)
    school = models.ForeignKey(
        School,
        on_delete=models.DO_NOTHING,
        related_name='staff',
    )
    account = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='staff',
    )
    has_account = models.BooleanField(default=False)

    def __str__(self):
        if len(self.other_names) == 0:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name} {self.last_name} {self.other_names}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_staff_id()
        super().save(*args, **kwargs)  # Call the original save method


class Qualification(models.Model):
    """Staff Academic & Professional Credentials"""
    CATEGORIES = (
        ('Academic', 'Academic'),
        ('Professional', 'Professional'),
    )
    category = models.CharField(max_length=255, choices=CATEGORIES)
    title = models.CharField(max_length=255)
    date_obtain = models.DateField()
    institution = models.CharField(max_length=255)
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='qualifications',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Promotion(models.Model):
    """Staff Promotions"""
    rank = models.CharField(max_length=255)
    notional_date = models.DateField(blank=True, null=True)
    substantive_date = models.DateField()
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='promotions',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.rank
