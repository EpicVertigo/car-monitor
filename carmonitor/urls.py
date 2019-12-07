from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from autoria.urls import router

urlpatterns = [
    path('', include('autoria.urls')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('openapi', get_schema_view(
        title="Car Monitor",
        description="API for working with AutoRia data",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='autoria/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
