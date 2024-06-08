from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from applications.user_profiles import models


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('More info'), {'fields': ('gender', 'birthday', 'avatar')}),
    )


admin.site.register(models.CustomUser, CustomUserAdmin)


@admin.register(models.UserPersonalData)
class UserPersonalDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'birthday', 'user')
    list_display_links = ('id', )


@admin.register(models.Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


@admin.register(models.Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'follower')
    list_display_links = ('id', 'user')


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'website',
        'github',
        'twitter',
        'instagram',
        'facebook'
    )
    list_display_links = ('id', 'user')
