from rest_framework import serializers
from autoria.models import *


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
