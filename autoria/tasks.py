import os
from subprocess import call

from autoria.models import MonitorQuery
from carmonitor.celery import app


@app.task()
def monitor_query(uuid):
    try:
        obj = MonitorQuery.objects.get(name=uuid)
        call(['scrapy', 'crawl', 'autoria', '-a', f'query={obj.query_string}'])
    except MonitorQuery.ObjectNotFound:
        return False
