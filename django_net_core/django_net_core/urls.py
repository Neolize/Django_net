"""
URL configuration for django_net_core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django_net_core import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('api/v1/', include('applications.user_profiles.urls')),
    path('', include('applications.frontend.urls')),
]


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
