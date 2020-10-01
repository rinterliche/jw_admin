from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from account.models import JWAdminUser
from .models import Territory, ServiceOccurrence
from .serializers import (
    TerritorySerializer,
    ServiceOccurrenceSerializer,
    JWAdminUserSerializer,
)


@api_view(
    [
        "GET",
    ]
)
def api_jwadminusers_view(request):
    territories = JWAdminUser.objects.all()
    serializer = JWAdminUserSerializer(territories, many=True)

    return Response(serializer.data)


@api_view(
    [
        "GET",
    ]
)
def api_service_occurrences_view(request):
    service_occurrences = ServiceOccurrence.objects.all()
    serializer = ServiceOccurrenceSerializer(service_occurrences, many=True)

    return Response(serializer.data)


@api_view(
    [
        "POST",
    ]
)
def api_new_service_occurrence_view(request):
    if request.method == "POST":
        service_occurrence = ServiceOccurrence()
        serializer = ServiceOccurrenceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "GET",
        "PUT",
        "DELETE",
    ]
)
def api_service_occurrence_view(request, id):
    try:
        service_occurrence = ServiceOccurrence.objects.get(id=id)
    except ServiceOccurrence.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ServiceOccurrenceSerializer(service_occurrence)

        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ServiceOccurrenceSerializer(service_occurrence, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data["success"] = "updated"

            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        operation = service_occurrence.delete()

        data = {}

        if operation:
            data["success"] = "deleted"

        return Response(data=data)


@api_view(
    [
        "GET",
    ]
)
def api_territories_view(request):
    territories = Territory.objects.all()
    serializer = TerritorySerializer(territories, many=True)

    return Response(serializer.data)


@api_view(
    [
        "POST",
    ]
)
def api_new_territory_view(request):
    if request.method == "POST":
        territory = Territory()
        serializer = TerritorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "GET",
        "PUT",
        "DELETE",
    ]
)
def api_territory_view(request, id):
    try:
        territory = Territory.objects.get(id=id)
    except Territory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TerritorySerializer(territory)

        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TerritorySerializer(territory, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data["success"] = "updated"

            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        operation = territory.delete()

        data = {}

        if operation:
            data["success"] = "deleted"

        return Response(data=data)
