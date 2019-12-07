import json
import logging
import time
from datetime import datetime

import pandas as pd
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from tqdm import tqdm

from autoria.models import *
from carmonitor.settings import AUTORIA_API_KEY


class AutoRiaDataController:

    category_ids = []
    api_suffix = f'?api_key={AUTORIA_API_KEY}'

    def __init__(self, *args, **kwargs):
        self.steps = [
            self.download_categories,
            self.download_category_related,
            self.download_models,
            self.download_geo_data,
            self.download_unrelated_models
        ]

    def _make_api_call(self, model):
        return requests.get(f'{model.api_url}{self.api_suffix}').json()

    def _make_api_category_call(self, model, category_id):
        time.sleep(1)
        url = model.api_url
        return requests.get(url.format(categoryId=category_id)+self.api_suffix).json()

    def _make_api_model_call(self, category_id, brand_id):
        time.sleep(1)
        url = TransportBrand.api_url
        return requests.get(url.format(categoryId=category_id, markId=brand_id)+self.api_suffix).json()

    def download_categories(self):
        data = self._make_api_call(TransportCategory)
        TransportCategory.objects.bulk_create([TransportCategory(**x) for x in data])
        self.category_ids = TransportCategory.objects.values_list('value', flat=True)

    def download_category_related(self):
        category_related_models = [TransportBodystyle, TransportBrand,
                                   TransportDriverType, TransportGearType, TransportOptions]
        for model in tqdm(category_related_models, desc='Downloading category related models'):
            for category_id in self.category_ids:
                data = self._make_api_category_call(model, category_id)
                model.objects.bulk_create([model(**x, category_id=category_id) for x in data])

    def download_models(self):
        all_data = []
        categories = [1]  # Только легковые
        for category in tqdm(categories, desc='Downloading Models from categories'):
            brand_ids = TransportBrand.objects.filter(category_id=category).values_list('value', flat=True)
            for brand in tqdm(list(brand_ids), desc='Downloading Models for Brands'):
                data = self._make_api_model_call(category, brand)
                data = [dict(category_id=category, brand_id=brand, **x) for x in data]
                all_data.extend(data)
        # Filter out duplicates
        filtered_data = pd.DataFrame(all_data).drop_duplicates(subset=['value', 'brand_id']).to_dict(orient='records')
        TransportModel.objects.bulk_create([TransportModel(**x) for x in filtered_data])

    def download_geo_data(self):
        state_data = requests.get(State.api_url+self.api_suffix).json()
        State.objects.bulk_create([State(**x) for x in state_data])
        state_ids = [x.get('value') for x in state_data]
        for state_id in state_ids:
            time.sleep(1)
            data = requests.get(City.api_url.format(stateId=state_id)+self.api_suffix).json()
            City.objects.bulk_create([City(**x, state_id=state_id) for x in data])

    def download_unrelated_models(self):
        for model in [TransportFuelType, TransportColors, TransportOrigin]:
            time.sleep(1)
            data = requests.get(model.api_url+self.api_suffix).json()
            model.objects.bulk_create([model(**x) for x in data])

    def run(self):
        for func in self.steps:
            func()


class Command(BaseCommand):
    help = 'Populates database with data from AutoRia API'

    def handle(self, *args, **options):
        AutoRiaDataController().run()
