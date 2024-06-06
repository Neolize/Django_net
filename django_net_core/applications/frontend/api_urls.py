from django.urls import path

from applications.user_profiles import views as up_views
from applications.groups import views as g_views


urlpatterns = [
    path('user/<int:pk>/', up_views.PublicUserDetailAPIView.as_view(), name='user_public_api'),
    path('user_list/', up_views.PublicUserListAPIView.as_view(), name='user_list_public_api'),
    path('group/<str:group_slug>/', g_views.PublicGroupDetailAPIView.as_view(), name='group_public_api'),
    path('group_list/', g_views.PublicGroupListAPIView.as_view(), name='group_list_public_api'),
]
