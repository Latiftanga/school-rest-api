"""Database models"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class School(models.Model):
    """School in the system"""
    name = models.CharField(max_length=64, unique=True)
    subdomain = models.CharField(max_length=64, unique=True)
    motto = models.CharField(max_length=255, blank=True, default='')
    logo = models.CharField(max_length=64, blank=True, default='')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    email = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_admin_account(self, email, password):
        """Create new school admin user account"""
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_staff_account(self, email, password):
        """Create new staff user account"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_student_account(self, email, password):
        """Create new student user account"""
        user = self.create_user(email, password)
        user.is_student = True
        user.save(using=self._db)
        return user

    def create_guardian_account(self, email, password):
        """Create new guardian user account"""
        user = self.create_user(email, password)
        user.is_guardian = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
