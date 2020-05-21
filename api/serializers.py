from account.models import JWAdminUser
from .models import Territory, ServiceOccurrence
from rest_framework import serializers


class TerritorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Territory
        fields = ['id', 'number', 'name', 'notes', 'map_url',]


class JWAdminUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = JWAdminUser
        fields = ['id', 'first_name', 'last_name', 'email',]


class ServiceOccurrenceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    date = serializers.DateField()

    class Meta:
        model = ServiceOccurrence
        fields = ['id', 'date', 'leader', 'territory', 'status', 'period',]

    def to_representation(self, instance):
        self.fields['leader'] = JWAdminUserSerializer(read_only=True)
        self.fields['territory'] = TerritorySerializer(read_only=True)
        return super(ServiceOccurrenceSerializer, self).to_representation(instance)
