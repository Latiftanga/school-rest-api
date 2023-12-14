from rest_framework import (
    serializers,
)

from staff import models


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for staff model"""

    category = serializers.ChoiceField(
        choices=('Teaching', 'Non Teaching')
    )

    gender = serializers.ChoiceField(
        choices=(('M', 'Male'), ('F', 'Female'))
    )

    class Meta:
        model = models.Staff

        fields = [
            'id',
            'category',
            'first_name',
            'last_name',
            'other_names',
            'gender',
            'date_of_birth',
            'place_of_birth',
            'home_town',
            'home_district',
            'home_region',
            'religion',
            'disability',
            'disability_description',
            'phone',
            'residential_address',
            'active',
        ]

        read_only_fields = [
            'id',
            'active',
        ]

    def validate(self, attrs):
        """Get the current login user school"""
        request = self.context.get('request')
        attrs['school'] = request.user.staff.school
        return attrs


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
