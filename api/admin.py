from django.contrib import admin
from .models import Territory, ServiceOccurrence


class TerritoryAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "name",
        "notes",
        "congregation",
    )
    search_fields = ("number", "name")

    ordering = ("number", "name")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ServiceOccurrenceAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "leader",
        "territory",
        "status",
        "period",
        "congregation",
    )
    search_fields = ("date",)

    ordering = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Territory, TerritoryAdmin)
admin.site.register(ServiceOccurrence, ServiceOccurrenceAdmin)
