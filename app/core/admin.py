"""Django admin custom customization"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    """Define teh admin pages for users."""
    ordering = ['email']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
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
                    'email',
                    'password1',
                    'password2',
                    'is_active',
                    'is_student',
                    'is_guardian',
                    'is_teacher',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
    )


admin.site.register(models.User, UserAdmin)
