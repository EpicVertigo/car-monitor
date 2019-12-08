from django.urls import path
from autoria.views import create_view
from autoria import viewsets
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'category', viewsets.TransportCategoryView)
router.register(r'brands', viewsets.TransportBrandView)
router.register(r'states', viewsets.StateViewSet)
router.register(r'extras', viewsets.ExtraViewSet, base_name='extra')

urlpatterns = [
    path('', create_view, name='create'),
    path('api/create_monitoring', viewsets.MonitorQueryView.as_view(), name='create_monitoring')
]
