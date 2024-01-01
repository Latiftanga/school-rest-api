"""Django admin custom customization"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models
from staff.models import Staff


class UserAdmin(BaseUserAdmin):
    """Define teh admin pages for users."""
    ordering = ['account_id']
    list_display = ['account_id']
    fieldsets = (
        (None, {'fields': ('account_id', 'password', 'email',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_admin',
                    'is_superuser',
                    'is_teacher',
                    'is_student',
                    'is_guardian',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    read_only_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'account_id',
                    'password1',
                    'password2',
                    'is_active',
                    'is_student',
                    'is_guardian',
                    'is_teacher',
                    'is_staff',
                    'is_admin',
                    'is_superuser',
                )
            }
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.School)
admin.site.register(Staff)
