from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from core.utils import generate_random_text

from rest_framework import (
    serializers,
)

from staff import models


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for staff model"""

    class Meta:
        model = models.Staff

        fields = [
            'id',
            'category',
            'registered_no',
            'sssnit_no',
            'license_no',
            'date_appointed',
            'first_name',
            'last_name',
            'other_names',
            'gender',
            'date_of_birth',
            'place_of_birth',
            'home_town',
            'home_district',
            'home_region',
            'nationality',
            'national_id',
            'religion',
            'disability',
            'disability_description',
            'phone',
            'email',
            'residential_address',
            'permanent_address',
            'digital_address',
            'postal_address',
            'has_account',
        ]
        read_only_fields = [
            'id',
            'active',
        ]

    def validate(self, attrs):
        """Get the current login user school"""
        user = self.context.get('request').user
        try:
            attrs['school'] = user.staff.school.id
        except ValueError:
            raise serializers.ValidationError(
              'You must be assign a school to perform this operation'
            )
        return attrs

    def create(self, validated_data):
        if validated_data.get('has_account', False):
            if validated_data.get('email') is None \
                    or validated_data.get('email') == '':
                raise serializers.ValidationError(
                    'Please provide a valid email'
                )
            staff = models.Staff.objects.create(**validated_data)
            password = generate_random_text(6)
            staff.account = get_user_model().objects.create_staff_account(
                account_id=staff.id,
                password=password
            )
            staff.account.email = staff.email
            staff.account.save()
            staff.save()
            try:
                send_mail(
                    'Account Credentials',
                    f'Your account credentials:\nID:\
                        {staff.account.id}\nPassword: \
                            {password}',
                    settings.EMAIL_HOST_USER,
                    [staff.account.email],
                    fail_silently=False,
                )
            except Exception as e:
                staff.account.delete()
                staff.delete()
                raise serializers.ValidationError(e)
            return staff
        return models.Staff.objects.create(**validated_data)


class PromotionSerializer(serializers.ModelSerializer):
    """Serializer for Promotion"""

    class Meta:
        model = models.Promotion
        fields = (
            'id',
            'rank',
            'notional_date',
            'substantive_date',
        )

        read_only_fields = ('id', )


class QualificationSerializer(serializers.ModelSerializer):
    """Serializer for Qualification"""

    class Meta:
        model = models.Qualification
        fields = (
            'id',
            'category',
            'title',
            'date_obtain',
            'institution',
        )

        read_only_fields = ('id', )


class StaffDetailSerializer(StaffSerializer):
    """Serializer for staff detail view"""

    qualifications = QualificationSerializer(
        many=True,
        read_only=True
    )
    promotions = PromotionSerializer(
        many=True,
        read_only=True
    )

    class Meta(StaffSerializer.Meta):
        fields = StaffSerializer.Meta.fields + [
            'qualifications',
            'promotions'
        ]
