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

    def create_user(self, account_id, password, **extra_fields):
        """Create, save and return a new user"""
        if not account_id:
            raise ValueError('User must have an Account ID')
        # user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(account_id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, account_id, password):
        """Create new superuser"""
        user = self.create_user(account_id, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_admin_account(self, account_id, password):
        """Create new school admin user account"""
        user = self.create_user(account_id, password)
        user.is_admin = True
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_staff_account(self, account_id, password):
        """Create new staff user account"""
        user = self.create_user(account_id, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_student_account(self, account_id, password):
        """Create new student user account"""
        user = self.create_user(account_id, password)
        user.is_student = True
        user.save(using=self._db)
        return user

    def create_guardian_account(self, account_id, password):
        """Create new guardian user account"""
        user = self.create_user(account_id, password)
        user.is_guardian = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    account_id = models.CharField(max_length=64, unique=True)
    email = models.EmailField(
        max_length=255, unique=True, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'account_id'


class Person(models.Model):
    """Personal Detail"""
    GENDER = [('M', 'Male'), ('F', 'Female')]
    RELIGON = [
        ('African Traditional Religion', 'African Traditional Religion'),
        ('Christian', 'Christian'),
        ('Islam', 'Islam'),
        ('Rastafarianism', 'Rastafarianism'),
        ('Judaism', 'Judaism'),
        ('Hinduism', 'Hinduism'),
        ('Other', 'Other'),
    ]
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    other_names = models.CharField(max_length=128, blank=True, default='')
    gender = models.CharField(max_length=1, choices=GENDER)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=128)
    home_town = models.CharField(max_length=128)
    home_district = models.CharField(max_length=128)
    home_region = models.CharField(max_length=128)
    nationality = models.CharField(max_length=128)
    national_id = models.CharField(
        max_length=64, blank=True, null=True,
    )
    religion = models.CharField(
        max_length=128, blank=True, default='', choices=RELIGON
    )
    disability = models.BooleanField(default=False)
    disability_description = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    phone = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(
        max_length=128, unique=True, blank=True, null=True
    )
    residential_address = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)
    digital_address = models.CharField(max_length=64, blank=True, default='')
    postal_address = models.CharField(max_length=255, blank=True, default='')
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
