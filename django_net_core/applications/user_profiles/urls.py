from django.urls import path

from applications.user_profiles import views


urlpatterns = [
    path("user/<int:pk>/", views.PublicCustomUserAPIViewSet.as_view({"get": "retrieve"})),
    path("user/private/<int:pk>/", views.PrivateCustomUserAPIViewSet.as_view({"get": "retrieve", "put": "update"})),
    path("user/personal-data/<int:pk>/", views.UserPersonalDataAPIViewSet.as_view({"get": "retrieve"})),
]
