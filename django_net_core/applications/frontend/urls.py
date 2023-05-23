from django.urls import path

from applications.frontend import views


urlpatterns = [
    path('', views.UsersView.as_view(), name='home'),

    path('user/', views.UserWallView.as_view(), name='user_wall'),
    path('user/profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('user/profile/edit_profile/<int:pk>/', views.EditUserProfileView.as_view(), name='edit_user_profile'),
    path('user/friends/', views.UserFriendsView.as_view(), name='user_friends'),

    path('login/', views.LoginUserView.as_view(), name='login'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]
