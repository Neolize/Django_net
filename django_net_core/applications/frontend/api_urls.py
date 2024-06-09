from django.urls import path

from applications.user_profiles import views as up_views
from applications.groups import views as g_views


urlpatterns = [
    path('user/<int:pk>/', up_views.PublicUserDetailAPIView.as_view(), name='user_public_api'),
    path('user-list/', up_views.PublicUserListAPIView.as_view(), name='user_list_public_api'),

    path('group/<str:group_slug>/', g_views.GroupDetailAPIView.as_view(), name='group_detail_api'),
    path('group-creation/', g_views.CreateGroupAPIView.as_view()),
    path('group-editing/<str:group_slug>/', g_views.UpdateGroupAPIView.as_view()),
    path('group-deletion/<str:group_slug>/', g_views.DeleteGroupAPIView.as_view()),
    path('group-list/', g_views.GroupListAPIView.as_view(), name='group_list_api'),
    path(
        'group-post/<str:group_post_slug>/',
        g_views.GroupPostDetailAPIView.as_view(),
        name='group_post_api'
    ),
    path('group-post-list/', g_views.GroupPostListAPIView.as_view()),
    path('group-member-list/', g_views.GroupMemberListAPIView.as_view()),
    path(
        'group-post-comments/<str:group_post_slug>/',
        g_views.GroupPostCommentListAPIView.as_view(),
        name='group_post_comment_api'
    ),
]
