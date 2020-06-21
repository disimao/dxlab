from django.urls import (
    path,
    include,
)
from django.views.generic import (
    TemplateView,
)
from rest_framework.schemas import (
    get_schema_view,
)


urlpatterns = [
    path('api/v1/', include('dxlab.apps.core.api.urls')),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/docs/swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}),
        name='swagger-ui'),
    path('openapi', get_schema_view(
        title="dxlab challenge",
        description="API for virtual store",
        version="1.0.0"
    ), name='openapi-schema'),
]
