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

    path('', include('applications.user_profiles.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
