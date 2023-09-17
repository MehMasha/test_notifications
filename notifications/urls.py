from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import ReDocRenderer, get_schema_view
from rest_framework import routers

from apps.clients.urls import router as clients_router
from apps.mailing.urls import router as mailing_router

with open('templates/notifications/description.html', 'r', encoding='utf-8') as file:
    description = file.read()

ReDocRenderer.template = 'notifications/custom_redoc.html'
schema_view = get_schema_view(
    openapi.Info(
        title="Notifications API",
        default_version='v1',
        description=description,
        contact=openapi.Contact(email="mehmasha69@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


router = routers.DefaultRouter()
router.registry.extend(clients_router.registry)
router.registry.extend(mailing_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'api'), namespace='api')),
    path(
        'docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='swagger-ui'
    ),
    path('', include('django_prometheus.urls')),
]
