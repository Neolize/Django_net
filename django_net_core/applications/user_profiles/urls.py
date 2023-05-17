from django.urls import path

from applications.user_profiles import views


urlpatterns = [
    path('', views.index)
]
