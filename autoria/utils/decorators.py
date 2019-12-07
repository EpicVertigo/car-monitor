from django.db.models import signals
from django_celery_beat.models import PeriodicTasks


def periodic_task(cls):
    """Helper decorator for connecting signals to PeriodicTasks.changed function"""
    signals.pre_delete.connect(PeriodicTasks.changed, sender=cls, dispatch_uid=cls.__name__)
    signals.pre_save.connect(PeriodicTasks.changed, sender=cls, dispatch_uid=cls.__name__)
    return cls
