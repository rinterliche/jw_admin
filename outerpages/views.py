import datetime
from datetime import (timedelta, date)

from django.shortcuts import render

from api.models import Territory, ServiceOccurrence
from account.models import JWAdminUser


def page_not_found_view(request, exception=None):
    """
    Get static asset for 404 error pages
    """
    return render(request, "outerpages/404.html", {})


def error_view(request, exception=None):
    """
    Get static asset for 500 error pages
    """
    return render(request, "outerpages/500.html", {})


def permission_denied_view(request, exception=None):
    """
    Get static asset for 403 error pages
    """
    return render(request, "outerpages/403.html", {})


def bad_request_view(request, exception=None):
    """
    Get static asset for 400 error pages
    """
    return render(request, "outerpages/400.html", {})


def service_week_screen_view(request):
    """
    Provide service week page resources, if user is authenticated
    """
    if request.user.is_authenticated:
        def _get_current_week_dates_list():
            """
            Return the full week (Sunday first) of the week containing the given date.
            'date' may be a datetime or date instance (the same type is returned).
            """
            today_date = datetime.datetime.now().date()
            one_day = datetime.timedelta(days=1)

            # turn sunday into 0, monday into 1, etc.
            day_idx = (today_date.weekday() + 1) % 7
            sunday = today_date - datetime.timedelta(days=day_idx)
            today_date = sunday

            for n in range(7):
                yield today_date
                today_date += one_day

        current_week_dates_list = list(
            _get_current_week_dates_list())
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
                for current_week_service_occurrence \
                in current_week_service_occurrences.filter(date=current_week_date):
                    week_day = {
                        "id": current_week_service_occurrence.id,
                        "date": current_week_service_occurrence.date,
                        "period": current_week_service_occurrence.period,
                        "leader": current_week_service_occurrence.leader.first_name,
                        "territory_number": current_week_service_occurrence.territory.number,
                        "territory_name": current_week_service_occurrence.territory.name,
                        "is_today": current_week_date == date.today(),
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
                    "is_today": current_week_date == date.today(),
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

    return render(request, "outerpages/not_authorized.html", {})


def list_territories_view(request):
    """
    Provide territories page resources, if user is authenticated
    """
    if request.user.is_authenticated:
        all_territories = Territory.objects.filter(congregation=request.user.congregation.id)

        territories = []

        for territory in all_territories:
            t_last_service_occurrence = ServiceOccurrence.objects.filter(
                territory_id=territory.id).last()
            last_service_occurrence_date = None
            t_is_forgotten = True

            if t_last_service_occurrence:
                date_30_days_ago = datetime.datetime.now() - timedelta(days=30)
                last_service_occurrence_date = t_last_service_occurrence.date
                t_is_forgotten = last_service_occurrence_date.strftime(
                    '%Y-%m-%d') <= date_30_days_ago.strftime('%Y-%m-%d')

            _territory = {
                "id": territory.id,
                "number": territory.number,
                "name": territory.name,
                "last_service_occurrence_date": last_service_occurrence_date,
                "is_forgotten": t_is_forgotten,
            }

            territories.append(_territory)

        return render(request, "outerpages/list_territories.html", {'territories': territories})

    return render(request, "outerpages/not_authorized.html", {})


def new_territory_view(request):
    """
    Provide new territory page resources, if user is authenticated
    """
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, "outerpages/new_territory.html", {})

    return render(request, "outerpages/not_authorized.html", {})


def show_territory_view(request, id):
    """
    Provide show territory page resources, if user is authenticated
    """
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

    return render(request, "outerpages/not_authorized.html", {})


def edit_territory_view(request, _id):
    """
    Provide edit territory page resources, if user is authenticated
    """
    if request.user.is_authenticated and request.user.is_staff:
        territory = Territory.objects.get(id=_id)
        return render(request, "outerpages/edit_territory.html", {"territory": territory})

    return render(request, "outerpages/not_authorized.html", {})


def list_service_occurrences_view(request):
    """
    Provide list service ocurrences page resources, if user is authenticated
    """
    if request.user.is_authenticated and request.user.is_staff:
        service_occurrences = ServiceOccurrence.objects.filter(
            congregation=request.user.congregation.id,
            date__range=[
                request.GET.get("from", "2000-01-01"),
                request.GET.get("until", "2999-01-01")
            ]
        )

        return render(
            request,
            "outerpages/list_service_occurrences.html",
            {
                "service_occurrences": service_occurrences
            }
        )

    return render(request, "outerpages/not_authorized.html", {})


def new_service_occurrence_view(request):
    """
    Provide new service occurrence page resources, if user is authenticated
    """
    if request.user.is_authenticated and request.user.is_staff:
        territories = Territory.objects.filter(
            congregation=request.user.congregation.id)
        leaders = JWAdminUser.objects.filter(
            congregation=request.user.congregation.id)

        return render(
            request,
            "outerpages/new_service_occurrence.html",
            {
                "territories": territories,
                "leaders": leaders
            }
        )

    return render(request, "outerpages/not_authorized.html", {})


def edit_service_occurrence_view(request, id):
    """
    Provide edit service occurrence page resources, if user is authenticated
    """
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

    return render(request, "outerpages/not_authorized.html", {})


def show_service_occurrence_view(request, id):
    """
    Provide show service occurrence page resources, if user is authenticated
    """
    if request.user.is_authenticated:
        service_occurrence = ServiceOccurrence.objects.get(id=id)
        territories = Territory.objects.filter(
            congregation=request.user.congregation.id)
        leaders = JWAdminUser.objects.filter(
            congregation=request.user.congregation.id)

        return render(
            request,
            "outerpages/show_service_occurrence.html",
            {
                "territories": territories,
                "leaders": leaders,
                "service_occurrence": service_occurrence
            }
        )

    return render(request, "outerpages/not_authorized.html", {})
