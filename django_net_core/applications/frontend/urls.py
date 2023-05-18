from django.urls import path

from applications.frontend import views


urlpatterns = [
    path('', views.index, name='home'),
]
