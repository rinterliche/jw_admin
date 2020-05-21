from django.db import models
from account.models import JWAdminUser
from enum import Enum


class Territory(models.Model):
    class Meta:
        verbose_name = "Território"
        verbose_name_plural = "Territórios"

    number = models.PositiveIntegerField()
    name = models.CharField(max_length=50, default='')
    map_url = models.CharField(max_length=250, default='')
    notes = models.TextField(default='')

    def __str__(self):
        return "Territory number: {}".format(self.number)


class ServiceOccurrence(models.Model):
    class Meta:
        verbose_name = "Saída de campo"
        verbose_name_plural = "Saídas de campo"

    NOT_INITIALIZED = 'N'
    INITIALIZED = 'I'
    FINALIZED = 'F'
    CONTINUED = 'C'
    STATUSES = (
        (NOT_INITIALIZED, 'N'),
        (INITIALIZED, 'I'),
        (FINALIZED, 'F'),
        (CONTINUED, 'C'),
    )

    MOURNING = 'M'
    AFTERNOON = 'A'
    PERIODS = (
        (MOURNING, 'M'),
        (AFTERNOON, 'A'),
    )

    leader = models.ForeignKey(JWAdminUser, on_delete=models.CASCADE)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=FINALIZED,
    )
    period = models.CharField(
        max_length=1,
        choices=PERIODS,
        default=MOURNING,
    )

    def __str__(self):
        return "Service Occurrence made at: {}, by {}".format(self.territory.number, self.leader)
