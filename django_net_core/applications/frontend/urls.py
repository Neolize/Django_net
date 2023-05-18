from django.urls import path

from applications.frontend import views


urlpatterns = [
    path('', views.index, name='home'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]
