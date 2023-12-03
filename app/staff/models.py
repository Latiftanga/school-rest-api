from django.db import models
from django.contrib.auth import get_user_model
from core.models import School


class Staff(models.Model):
    """staff in the system"""
    category = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    other_names = models.CharField(max_length=32, blank=True, default='')
    gender = models.CharField(max_length=8)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=32)
    home_town = models.CharField(max_length=32)
    home_district = models.CharField(max_length=32)
    home_region = models.CharField(max_length=32)
    nationality = models.CharField(max_length=32)
    religion = models.CharField(max_length=32, blank=True, default='')
    disability = models.BooleanField(default=False)
    disability_description = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    phone = models.CharField(
        max_length=32,
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
        related_name='staffs',
        related_query_name='staff_list'
    )

    def __str__(self):
        if len(self.other_names) == 0:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name} {self.last_name} {self.other_names}'
