from django.urls import path

from applications.user_profiles import views as up_views


urlpatterns = [
    path('user/<int:pk>/', up_views.PublicCustomUserAPIViewSet.as_view({'get': 'retrieve'}), name='user_public_api'),
    path('private/user/<int:pk>/', up_views.PrivateCustomUserAPIViewSet.as_view({'get': 'retrieve'})),
]
