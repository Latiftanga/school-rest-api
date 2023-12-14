from django.db import models
from django.contrib.auth import get_user_model
from core.models import School


class Staff(models.Model):
    """staff in the system"""
    category = models.CharField(max_length=128)
    staff_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )
    registered_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )
    sssnit_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )
    license_no = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )
    date_appointed = models.DateField(
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    other_names = models.CharField(max_length=128, blank=True, default='')
    gender = models.CharField(max_length=64)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=128)
    home_town = models.CharField(max_length=128)
    home_district = models.CharField(max_length=128)
    home_region = models.CharField(max_length=128)
    nationality = models.CharField(max_length=128)
    religion = models.CharField(max_length=128, blank=True, default='')
    disability = models.BooleanField(default=False)
    disability_description = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    phone = models.CharField(
        max_length=64,
        unique=True,
    )
    residential_address = models.CharField(max_length=255)
    account = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='staff',
    )
    active = models.BooleanField(default=True)
    school = models.ForeignKey(
        School,
        on_delete=models.DO_NOTHING,
        related_name='staff_list',
    )

    def __str__(self):
        if len(self.other_names) == 0:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name} {self.last_name} {self.other_names}'


class Qualification(models.Model):
    """Staff Academic & Professional Credentials"""
    category = models.CharField(max_length=255)
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
