from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view, ReDocRenderer
from drf_yasg import openapi
# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


ReDocRenderer.template = 'notifications/custom_redoc.html'
schema_view = get_schema_view(
    openapi.Info(
        title="Notifications API",
        default_version='v1',
        description="Django Project API",
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
    # path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]
