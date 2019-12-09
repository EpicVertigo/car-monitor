from scrapy_djangoitem import DjangoItem
from autoria.models import MonitorResult, MonitorPriceChangeEvent


class CarscraperItem(DjangoItem):
    django_model = MonitorResult
