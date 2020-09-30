from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import JWAdminUser, JWAdminCongregation


class JWAdminCongregationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class JWAdminUserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'is_staff')
    list_filter = ('is_admin',)
    search_fields = ('first_name', 'last_name')

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(JWAdminUser, JWAdminUserAdmin)
admin.site.register(JWAdminCongregation, JWAdminCongregationAdmin)
