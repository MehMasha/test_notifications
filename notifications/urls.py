from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view, ReDocRenderer
from drf_yasg import openapi
# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


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
    # permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
