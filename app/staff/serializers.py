from rest_framework import (
    serializers,
)

from staff import models
from core import permissions


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for staff model"""

    class Meta:
        model = models.Staff

    permission_classes = [
        permissions.IsAdmin
    ]

    fields = [
        'id',
        'first_name',
        'last_name',
        'other_names',
        'gender',
        'date_of_birth',
        'place_of_birth',
        'home_town',
        'home_district'
        'home_region',
        'religion',
        'disability',
        'disability_description',
        'phone',
        'residential_address',
        'active',
        'school',
        'account',

    ]

    read_only_fields = [
        'id',
        'active'
    ]
