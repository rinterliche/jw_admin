from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import JWAdminUser, JWAdminCongregation


class JWAdminUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'is_staff')
    search_fields = ('first_name', 'last_name')

    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class JWAdminCongregationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(JWAdminUser, JWAdminUserAdmin)
admin.site.register(JWAdminCongregation, JWAdminCongregationAdmin)
