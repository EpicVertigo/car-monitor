from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from autoria.models import (State, TransportBrand, TransportCategory,
                            TransportColors, TransportFuelType,
                            TransportOrigin)
from autoria.serializers import (StateDetailSerializer, StateListSerializer,
                                 TransportBrandDetailSerializer,
                                 TransportBrandListSerializer,
                                 TransportCategoryDetailsSerializer,
                                 TransportCategoryListSerializer,
                                 TransportColorSerializer,
                                 TransportFuelTypeSerializer,
                                 TransportOriginSerializer)


class MultipleSerializersMixin:
    detail_serializer = None

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        if self.action == 'retrieve':
            return self.detail_serializer
        return self.serializer_class


class OriginViewSet(viewsets.ModelViewSet):
    queryset = TransportOrigin.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransportOriginSerializer


class FuelTypeViewSet(viewsets.ModelViewSet):
    queryset = TransportFuelType.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransportFuelTypeSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = TransportColors.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransportColorSerializer


class StateViewSet(MultipleSerializersMixin, viewsets.ModelViewSet):
    queryset = State.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StateListSerializer
    detail_serializer = StateDetailSerializer


class TransportBrandView(MultipleSerializersMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = TransportBrand.objects.all()
    serializer_class = TransportBrandListSerializer
    detail_serializer = TransportBrandDetailSerializer


class TransportCategoryView(MultipleSerializersMixin, viewsets.ModelViewSet):
    queryset = TransportCategory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransportCategoryListSerializer
    detail_serializer = TransportCategoryDetailsSerializer
