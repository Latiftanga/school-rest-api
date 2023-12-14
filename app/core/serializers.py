"""Serializers for the core app"""
from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from staff.serializers import StaffDetailSerializer


class UserAccountSerializer (
    serializers.ModelSerializer
):
    """Serializer for creating teacher user account"""

    class Meta:
        model = get_user_model()
        fields = ['email', ]

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            **validated_data
        )


class UpdateUserAccountSerializer (
    serializers.ModelSerializer
):
    """Serializer for updating user account"""

    profile = serializers.SerializerMethodField(
        method_name='get_user_profile',
        read_only=True,
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def get_user_profile(self, user):
        if user.is_teacher:
            return StaffDetailSerializer(user.staff).data
        if user.is_student:
            return 'Student Details Here'
        if user.is_guardian:
            return 'Guardian Details Here'
        return 'None'


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validates and authenticate the user"""
        email = attrs['email']
        password = attrs['password']
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
