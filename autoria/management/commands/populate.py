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

    category_ids = [1]
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
        url = TransportModel.api_url
        return requests.get(url.format(categoryId=category_id, markId=brand_id)+self.api_suffix).json()

    def download_categories(self):
        data = self._make_api_call(TransportCategory)
        TransportCategory.objects.bulk_create([TransportCategory(id=x['value'], name=x['name']) for x in data])

    def download_category_related(self):
        category_related_models = [TransportBodystyle, TransportBrand,
                                   TransportDriverType, TransportGearType, TransportOptions]
        for model in tqdm(category_related_models, desc='Downloading category related models'):
            model_data = []
            for category_id in self.category_ids:
                model_data.extend(self._make_api_category_call(model, category_id))

            filtered_data = (pd.DataFrame(model_data)
                             .assign(category_id=category_id)
                             .drop_duplicates(subset=['value', 'category_id'])
                             .rename(columns={'value': 'id'})
                             .to_dict(orient='records'))
            model.objects.bulk_create([model(**x) for x in filtered_data])

    def download_models(self):
        all_data = []
        categories = [1]  # Только легковые
        for category in tqdm(categories, desc='Downloading Models from categories'):
            brand_ids = TransportBrand.objects.filter(category_id=category).values_list('id', flat=True)
            for brand in tqdm(list(brand_ids), desc='Downloading Models for Brands'):
                data = self._make_api_model_call(category, brand)
                data = [dict(category_id=category, brand_id=brand, id=x['value'], name=x['name']) for x in data]
                all_data.extend(data)
        # Filter out duplicates
        filtered_data = pd.DataFrame(all_data).drop_duplicates(subset=['id', 'brand_id']).to_dict(orient='records')
        TransportModel.objects.bulk_create([TransportModel(**x) for x in filtered_data])

    def download_geo_data(self):
        state_data = requests.get(State.api_url+self.api_suffix).json()
        State.objects.bulk_create([State(id=x['value'], name=x['name']) for x in state_data])
        state_ids = [x.get('id') for x in state_data]
        for state_id in state_ids:
            time.sleep(1)
            data = requests.get(City.api_url.format(stateId=state_id)+self.api_suffix).json()
            City.objects.bulk_create([City(id=x['value'], name=x['name'], state_id=state_id) for x in data])

    def download_unrelated_models(self):
        for model in [TransportFuelType, TransportColors, TransportOrigin]:
            time.sleep(1)
            data = requests.get(model.api_url+self.api_suffix).json()
            model.objects.bulk_create([model(id=x['value'], name=x['name']) for x in data])

    def run(self):
        for func in self.steps:
            func()


class Command(BaseCommand):
    help = 'Populates database with data from AutoRia API'

    def handle(self, *args, **options):
        AutoRiaDataController().run()
