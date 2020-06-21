from django.urls import (
    path,
    include,
)

urlpatterns = [
    path('api/', include('dxlab.apps.core.api.urls')),
]
