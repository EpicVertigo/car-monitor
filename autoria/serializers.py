from urllib.parse import urlencode
from uuid import uuid4

import requests
from rest_framework import serializers
from rest_framework.response import Response

from autoria.models import *
from carmonitor.settings import AUTORIA_API_KEY


class MonitorQuerySerializer(serializers.Serializer):
    base_url = 'https://developers.ria.com/auto/search?api_key={key}&{query}'
    category_id = serializers.IntegerField(required=True)
    marka_id = serializers.IntegerField(required=True)
    model_id = serializers.IntegerField(required=True)
    gearbox = serializers.IntegerField()
    bodystyle = serializers.IntegerField()

    def _create_api_urls(self, key=AUTORIA_API_KEY) -> str:
        data = {f'{key}[0]': value for key, value in self.data.items() if isinstance(value, int)}
        query = urlencode(data)
        return self.base_url.format(key=key, query=query)

    def check_url(self, url: str, user=None):
        r = requests.get(url)
        if 200 <= r.status_code < 400:
            data = r.json()
            results = data.get('result').get('search_result').get('ids')
            if len(results) == 0:
                return Response('No results for given query', status=400)
            MonitorQuery.objects.create(
                task=MonitorQuery.default_task,
                user=user,
                url=url,
                name=uuid4(),
                interval_id=1
            )
            return Response('Success', status=200)
        return Response(r.json(), status=r.status_code)

    def create_monitoring(self, user=None, **kwargs):
        return self.check_url(self._create_api_urls(), user=user)


class TransportColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportColors
        fields = '__all__'


class TransportOriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportOrigin
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class StateDetailSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True)

    class Meta:
        model = State
        fields = ['id', 'name', 'cities']


class StateListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = State
        fields = ['id', 'name', 'url']


class TransportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportModel
        fields = ['id', 'name']


class BodystyleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TransportBodystyle
        fields = ['id', 'name']


class TransportDriverTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportDriverType
        fields = '__all__'


class TransportFuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportFuelType
        fields = '__all__'


class TransportGearTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportGearType
        fields = '__all__'


class TransportOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportOptions
        fields = '__all__'


class TransportBrandListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TransportBrand
        fields = ['url', 'id', 'name']


class TransportBrandDetailSerializer(serializers.ModelSerializer):
    models = TransportModelSerializer(many=True)

    class Meta:
        model = TransportBrand
        fields = ['url', 'id', 'name', 'category_id', 'models']


class TransportCategoryListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TransportCategory
        fields = ['url', 'name', 'id']


class TransportCategoryDetailsSerializer(serializers.ModelSerializer):

    bodystyles = BodystyleSerializer(many=True)
    brands = TransportBrandListSerializer(many=True)
    drivertypes = TransportDriverTypeSerializer(many=True)
    geartypes = TransportGearTypeSerializer(many=True)
    options = TransportOptionsSerializer(many=True)

    class Meta:
        model = TransportCategory
        fields = ['name', 'id', 'bodystyles', 'brands', 'drivertypes', 'geartypes', 'options']
