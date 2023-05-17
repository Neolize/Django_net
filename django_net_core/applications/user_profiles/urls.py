from django.urls import path

from applications.user_profiles import views


urlpatterns = [
    path('user/<int:pk>/', views.PublicCustomUserAPIViewSet.as_view({'get': 'retrieve'})),
    path('private/user/<int:pk>/', views.PrivateCustomUserAPIViewSet.as_view({'get': 'retrieve'})),
]
