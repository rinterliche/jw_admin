import json
import json
import datetime
from datetime import timedelta

from django.shortcuts import render
from django.template import RequestContext
from django.views.defaults import page_not_found

from api.models import Territory, ServiceOccurrence
from account.models import JWAdminUser


def page_not_found_view(request, exception=None):
    return render(request,"outerpages/404.html", {})


def error_view(request, exception=None):
    return render(request, "outerpages/500.html", {})


def permission_denied_view(request, exception=None):
    return render(request, "outerpages/403.html", {})


def bad_request_view(request, exception=None):
    return render(request, "outerpages/400.html", {})


def service_week_screen_view(request):
    def _get_current_week_dates_list(date):
        """
        Return the full week (Sunday first) of the week containing the given date.
        'date' may be a datetime or date instance (the same type is returned).
        """
        one_day = datetime.timedelta(days=1)
        # turn sunday into 0, monday into 1, etc.
        day_idx = (date.weekday() + 1) % 7
        sunday = date - datetime.timedelta(days=day_idx)
        date = sunday

        for n in range(7):
            yield date
            date += one_day

    if request.user.is_authenticated:
        current_week_dates_list = list(_get_current_week_dates_list(datetime.datetime.now().date()))
        first_day_of_current_week = current_week_dates_list[0]
        last_day_of_current_week = current_week_dates_list[-1]

        current_week_service_occurrences = ServiceOccurrence.objects.filter(
            date__range=[first_day_of_current_week, last_day_of_current_week])

        current_week_service_occurrences_days = [
            current_week_service_occurrence.date
            for current_week_service_occurrence
            in current_week_service_occurrences
        ]

        current_week = []

        for current_week_date in current_week_dates_list:
            if current_week_date in current_week_service_occurrences_days:
                for current_week_service_occurrence in current_week_service_occurrences.filter(date=current_week_date):
                    week_day = {
                        "id": current_week_service_occurrence.id,
                        "date": current_week_service_occurrence.date,
                        "period": current_week_service_occurrence.period,
                        "leader": current_week_service_occurrence.leader.first_name,
                        "territory_number": current_week_service_occurrence.territory.number,
                        "territory_name": current_week_service_occurrence.territory.name,
                        "status": current_week_service_occurrence.status,
                    }

                    current_week.append(week_day)
            else:
                week_day = {
                    "id": None,
                    "date": current_week_date,
                    "period": "-",
                    "leader": "-",
                    "territory_number": "-",
                    "territory_name": "-",
                    "status": "-",
                }

                current_week.append(week_day)

        return render(
            request,
            "outerpages/service_week.html",
            {
                "current_week": current_week,
                "first_day_of_current_week": first_day_of_current_week,
                "last_day_of_current_week": last_day_of_current_week
            }
        )
    else:
        return render(request, "outerpages/not_authorized.html", {})


def list_territories_view(request):
    if request.user.is_authenticated:
        all_territories = Territory.objects.filter(congregation=request.user.congregation.id)

        territories = []

        for t in all_territories:
            t_last_service_occurrence = ServiceOccurrence.objects.filter(territory_id=t.id).last()
            last_service_occurrence_date = None
            t_is_forgotten = True

            if t_last_service_occurrence:
                date_30_days_ago = datetime.datetime.now() - timedelta(days=30)
                last_service_occurrence_date = t_last_service_occurrence.date
                t_is_forgotten = last_service_occurrence_date.strftime(
                    '%Y-%m-%d') <= date_30_days_ago.strftime('%Y-%m-%d')

            territory = {
                "id": t.id,
                "number": t.number,
                "name": t.name,
                "last_service_occurrence_date": last_service_occurrence_date,
                "is_forgotten": t_is_forgotten,
            }

            territories.append(territory)

        return render(request, "outerpages/list_territories.html", {'territories': territories})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def new_territory_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "outerpages/new_territory.html", {})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def show_territory_view(request, id):
    if request.user.is_authenticated:
        territory = Territory.objects.get(id=id)
        last_service_occurrences = ServiceOccurrence.objects.filter(
            territory_id=territory.id)[:5]
        return render(
            request,
            "outerpages/show_territory.html",
            {
                "territory": territory,
                "last_service_occurrences": last_service_occurrences
            }
        )
    else:
        return render(request, "outerpages/not_authorized.html", {})


def edit_territory_view(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        territory = Territory.objects.get(id=id)
        return render(request, "outerpages/edit_territory.html", {"territory": territory})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def list_service_occurrences_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        service_occurrences = ServiceOccurrence.objects.filter(
            congregation=request.user.congregation.id,
            date__range=[request.GET.get("from", "2000-01-01"), request.GET.get("until", "2999-01-01")]
        )
        return render(request, "outerpages/list_service_occurrences.html", {"service_occurrences": service_occurrences})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def new_service_occurrence_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        territories = Territory.objects.filter(
            congregation=request.user.congregation.id)
        leaders = JWAdminUser.objects.filter(
            congregation=request.user.congregation.id)
        return render(request, "outerpages/new_service_occurrence.html", {"territories": territories, "leaders": leaders})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def edit_service_occurrence_view(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        service_occurrence = ServiceOccurrence.objects.get(id=id)
        territories = Territory.objects.filter(
            congregation=request.user.congregation.id)
        leaders = JWAdminUser.objects.filter(
            congregation=request.user.congregation.id)

        return render(
            request,
            "outerpages/edit_service_occurrence.html",
            {
                "territories": territories,
                "leaders": leaders,
                "service_occurrence": service_occurrence
            }
        )
    else:
        return render(request, "outerpages/not_authorized.html", {})


def show_service_occurrence_view(request, id):
    if request.user.is_authenticated:
        service_occurrence = ServiceOccurrence.objects.get(id=id)
        territories = Territory.objects.filter(
            congregation=request.user.congregation.id)
        leaders = JWAdminUser.objects.filter(
            congregation=request.user.congregation.id)

        return render(
            request,
            "outerpages/show_service_occurrence.html",
            {"territories": territories, "leaders": leaders, "service_occurrence": service_occurrence}
        )
    else:
        return render(request, "outerpages/not_authorized.html", {})
