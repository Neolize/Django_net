from django.urls import path

from applications.frontend import views


urlpatterns = [
    path('', views.UsersView.as_view(), name='home'),

    path('user/', views.UserWallView.as_view(), name='user_wall'),
    path('user/profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('user/profile/edit_profile/<int:pk>/', views.EditUserProfileView.as_view(), name='edit_user_profile'),
    path('user/profile/create_post/', views.CreateUserPostView.as_view(), name='create_user_post'),
    path('user/profile/edit_post/<slug:slug>/', views.EditUserPostView.as_view(), name='edit_user_post'),
    path('user/profile/follow/<int:pk>/', views.follow_user, name='follow_user'),
    path('user/profile/unfollow/<int:pk>/', views.unfollow_user, name='unfollow_user'),

    path('group/<slug:group_slug>/', views.GroupView.as_view(), name='group'),
    path('user/<int:pk>/create_group/', views.GroupCreationView.as_view(), name='create_group'),

    path('user/friends/', views.UserFollowersView.as_view(), name='user_friends'),
    path('user/chat/<int:pk>/', views.UserChatView.as_view(), name='user_chat'),
    path('user/chat_list/', views.UserChatListView.as_view(), name='user_chat_list'),

    path('search/', views.PeopleSearchView.as_view(), name='people_search'),

    path('login/', views.LoginUserView.as_view(), name='login'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]
