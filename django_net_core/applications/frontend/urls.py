from django.urls import path

from applications.frontend import views


urlpatterns = [
    path('', views.UsersView.as_view(), name='home'),

    path('user/', views.UserWallView.as_view(), name='user_wall'),
    path('user/profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('user/profile/edit_profile/<int:pk>/', views.EditUserProfileView.as_view(), name='edit_user_profile'),
    path('user/profile/<int:pk>/user_comment/', views.handle_user_comment, name='handle_user_comment'),
    path('user/profile/create_post/', views.CreateUserPostView.as_view(), name='create_user_post'),
    path('user/profile/edit_post/<slug:slug>/', views.EditUserPostView.as_view(), name='edit_user_post'),
    path('user/profile/follow/<int:pk>/', views.follow_user, name='follow_user'),
    path('user/profile/unfollow/<int:pk>/', views.unfollow_user, name='unfollow_user'),
    path('user/profile/<slug:user_post_slug>/delete_user_post/', views.delete_user_post, name='delete_user_post'),
    path('user/profile/<int:pk>/delete_account/', views.delete_user_account, name='delete_user_account'),
    path('delete_user_comment/<int:comment_pk>/', views.delete_user_comment, name='delete_user_comment'),

    path('group/<slug:group_slug>/create_group_post/', views.CreateGroupPostView.as_view(), name='create_group_post'),
    path('group/edit_group_post/<slug:group_post_slug>/', views.EditGroupPostView.as_view(), name='edit_group_post'),
    path('group/<slug:group_slug>/', views.GroupView.as_view(), name='group'),
    path('group/<slug:group_slug>/group_comment/', views.handle_group_comment, name='handle_group_comment'),
    path('user/<int:pk>/create_group/', views.GroupCreationView.as_view(), name='create_group'),
    path('group/<slug:group_slug>/follow/', views.follow_group, name='follow_group'),
    path('group/<slug:group_slug>/unfollow/', views.unfollow_group, name='unfollow_group'),
    path('group/<slug:group_slug>/group_followers/', views.GroupFollowersView.as_view(), name='group_followers'),
    path('group/<slug:group_post_slug>/delete_group_post/', views.delete_group_post, name='delete_group_post'),
    path('group/<slug:group_slug>/delete_group/', views.delete_group, name='delete_group'),
    path('delete_group_comment/<int:comment_pk>/', views.delete_group_comment, name='delete_group_comment'),

    path('user/<int:pk>/followers/', views.UserFollowersView.as_view(), name='user_followers'),
    path('user/<int:pk>/following/', views.UserFollowingView.as_view(), name='user_following'),
    path('user/<int:pk>/groups/', views.UserGroupsView.as_view(), name='user_groups'),
    path('user/chat/<int:pk>/', views.UserChatView.as_view(), name='user_chat'),
    path('user/chat_list/', views.UserChatListView.as_view(), name='user_chat_list'),

    path('search/', views.PeopleSearchView.as_view(), name='people_search'),
    path('groups_search/', views.GroupSearchView.as_view(), name='group_search'),
    path('posts_search/', views.PostsSearchView.as_view(), name='posts_search'),

    path('login/', views.LoginUserView.as_view(), name='login'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]
