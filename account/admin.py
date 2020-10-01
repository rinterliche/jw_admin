from django.contrib import admin
from django import forms
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import JWAdminUser, JWAdminCongregation
from .forms import RegistrationForm, UserChangeForm


class JWAdminCongregationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class JWAdminUserAdmin(auth_admin.UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = RegistrationForm
    change_password_form = auth_admin.AdminPasswordChangeForm


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
            'fields': ('first_name', 'last_name', 'congregation', 'email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    search_fields = ('email', 'first_name', 'last_name', 'congregation',)
    ordering = ('email', 'first_name', 'last_name', 'congregation',)
    filter_horizontal = ()


admin.site.register(JWAdminUser, JWAdminUserAdmin)
admin.site.register(JWAdminCongregation, JWAdminCongregationAdmin)
