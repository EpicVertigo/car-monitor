from django.contrib import admin
from django_celery_beat.admin import PeriodicTaskAdmin

from autoria.models import MonitorQuery


@admin.register(MonitorQuery)
class MonitorQueryAdmin(PeriodicTaskAdmin):
    pass
