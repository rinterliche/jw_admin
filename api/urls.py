from django.urls import path
from api.views import(
    api_jwadminusers_view,

	api_service_occurrences_view,
    api_new_service_occurrence_view,
    api_service_occurrence_view,

    api_territories_view,
    api_new_territory_view,
    api_territory_view,
)

app_name = 'api'

urlpatterns = [
    path('jwadmin_user/list/', api_jwadminusers_view, name="jwadmin_users"),

    path('service_ocurrence/list/', api_service_occurrences_view, name="service_occurrences"),
    path('service_ocurrence/new/', api_new_service_occurrence_view, name="new_service_occurrence"),
    path('service_ocurrence/<id>/', api_service_occurrence_view, name="service_occurrence"),

    path('territory/list/', api_territories_view, name="territories"),
    path('territory/new/', api_new_territory_view, name="new_territories"),
    path('territory/<id>/', api_territory_view, name="territory"),
]
