from django.urls import path
from .views import index
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('', index),
    path('openapi/', get_schema_view(
        title="Reverse App",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
]