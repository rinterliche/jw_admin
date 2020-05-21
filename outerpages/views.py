from django.shortcuts import render
import json, datetime

from api.models import Territory, ServiceOccurrence
from account.models import JWAdminUser


def service_week_screen_view(request):
    def get_current_week_dates_list(date):
        """
        Return the full week (Sunday first) of the week containing the given date.
        'date' may be a datetime or date instance (the same type is returned).
        """
        one_day = datetime.timedelta(days=1)
        day_idx = (date.weekday() + 1) % 7  # turn sunday into 0, monday into 1, etc.
        sunday = date - datetime.timedelta(days=day_idx)
        date = sunday

        for n in range(7):
            yield date
            date += one_day

    current_week_dates_list = list(get_current_week_dates_list(datetime.datetime.now().date()))
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


def list_territories_view(request):
    territories = Territory.objects.all()
    return render(request, "outerpages/list_territories.html", {'territories': territories})


def new_territory_view(request):
    if request.user.is_staff:
        return render(request, "outerpages/new_territory.html", {})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def show_territory_view(request, id):
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


def edit_territory_view(request, id):
    if request.user.is_staff:
        territory = Territory.objects.get(id=id)
        return render(request, "outerpages/edit_territory.html", {"territory": territory})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def list_service_occurrences_view(request):
    if request.user.is_staff:
        service_occurrences = ServiceOccurrence.objects.all()
        return render(request, "outerpages/list_service_occurrences.html", {"service_occurrences": service_occurrences})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def new_service_occurrence_view(request):
    if request.user.is_staff:
        territories = Territory.objects.all()
        leaders = JWAdminUser.objects.all()
        return render(request, "outerpages/new_service_occurrence.html", {"territories": territories, "leaders": leaders})
    else:
        return render(request, "outerpages/not_authorized.html", {})


def edit_service_occurrence_view(request, id):
    if request.user.is_staff:
        service_occurrence = ServiceOccurrence.objects.get(id=id)
        territories = Territory.objects.all()
        leaders = JWAdminUser.objects.all()

        return render(
            request,
            "outerpages/edit_service_occurrence.html",
            {"territories": territories, "leaders": leaders, "service_occurrence": service_occurrence}
        )
    else:
        return render(request, "outerpages/not_authorized.html", {})


def show_service_occurrence_view(request, id):
    service_occurrence = ServiceOccurrence.objects.get(id=id)
    territories = Territory.objects.all()
    leaders = JWAdminUser.objects.all()

    return render(
        request,
        "outerpages/show_service_occurrence.html",
        {"territories": territories, "leaders": leaders, "service_occurrence": service_occurrence}
    )
