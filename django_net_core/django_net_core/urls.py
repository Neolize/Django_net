"""
URL configuration for django_net_core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from django_net_core import settings
from django_net_core.yasg import urlpatterns as yasg_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/', include('applications.frontend.api_urls')),
    path('', include('applications.frontend.urls')),
]

urlpatterns += yasg_urlpatterns

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
