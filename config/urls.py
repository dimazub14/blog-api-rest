from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("_status/", include("health_check.urls")),
]

# API URLS
urlpatterns += [
    # API base url
]

if not settings.DISABLE_ADMIN_PANEL:
    urlpatterns = [path(settings.ADMIN_URL, admin.site.urls)] + urlpatterns
if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar  # noqa E0401

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

        if settings.MEDIA_URL.startswith("/"):
            urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SWAGGER_ENABLED:
    # Swagger
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # Optional UI:
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
