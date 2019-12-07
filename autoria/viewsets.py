from rest_framework import mixins, permissions, viewsets
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


class SimpleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Simple ViewSet with ability to use additional serializer for `detail view`
    Only `list` and `retrieve` actions are allowed
    """
    detail_serializer = None

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        if self.action == 'retrieve':
            return self.detail_serializer
        return self.serializer_class


class StateViewSet(SimpleViewSet):
    queryset = State.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StateListSerializer
    detail_serializer = StateDetailSerializer


class TransportBrandView(SimpleViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = TransportBrand.objects.all()
    serializer_class = TransportBrandListSerializer
    detail_serializer = TransportBrandDetailSerializer


class TransportCategoryView(SimpleViewSet):

    queryset = TransportCategory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TransportCategoryListSerializer
    detail_serializer = TransportCategoryDetailsSerializer


class ExtraViewSet(viewsets.ViewSet):
    """
    Return a list of all additional fields, unrelated to car categories.
    """
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']

    def list(self, request):
        origin_data = TransportOriginSerializer(instance=TransportOrigin.objects.all(), many=True).data
        fuel_data = TransportFuelTypeSerializer(instance=TransportFuelType.objects.all(), many=True).data
        colors_data = TransportColorSerializer(instance=TransportColors.objects.all(), many=True).data
        return Response({
            'fueltypes': fuel_data,
            'colors': colors_data,
            'origin': origin_data
        })
