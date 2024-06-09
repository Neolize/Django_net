from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from applications.frontend.services import pagination
from applications.frontend.permissions import IsGroupCreator
from applications.groups import serializers
from applications.groups.services.crud import read, create, update, delete


class GroupDetailAPIView(APIView):
    serializer = serializers.GroupDetailSerializer

    def get(self, request: Request, group_slug: str):
        group = read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        serializer = self.serializer(group)
        return Response(serializer.data)


class GroupListAPIView(generics.ListAPIView):
    queryset = read.get_all_groups()
    serializer_class = serializers.GroupListSerializer
    pagination_class = pagination.GroupAPIListPagination


class CreateGroupAPIView(APIView):
    serializer = serializers.GroupCreationSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request: Request):
        serializer = create.create_new_group_from_api_request(
            request=request,
            serializer=self.serializer
        )
        if not serializer:
            return Response({'error': 'You cannot own more than 5 groups.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupPostDetailAPIView(APIView):
    serializer = serializers.GroupPostDetailSerializer

    def get(self, request: Request, group_post_slug: str):
        post = read.fetch_group_post_with_comments(group_post_slug)
        if not post:
            raise Http404

        serializer = self.serializer(post)
        return Response(serializer.data)


class GroupPostCommentListAPIView(generics.ListAPIView):
    serializer_class = serializers.GroupPostCommentListSerializer
    pagination_class = pagination.GroupPostCommentListPagination

    def get_queryset(self):
        return read.get_all_comments_for_group_post_by_slug(self.kwargs.get('group_post_slug', ''))


class UpdateGroupAPIView(APIView):
    serializer = serializers.GroupEditingSerializer
    permission_classes = (IsAuthenticated, IsGroupCreator)

    def put(self, request: Request, group_slug: str):
        group = read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        serializer = update.update_group_from_api_request(
            request=request,
            serializer=self.serializer,
            instance=group
        )
        if not serializer:
            return Response({'error': 'The fields weren\'t given.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class DeleteGroupAPIView(APIView):
    serializer = serializers.GroupDeletionSerializer
    permission_classes = (IsAuthenticated, IsGroupCreator)

    def delete(self, request: Request, group_slug: str):
        group = read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        serializer = delete.delete_group_from_api_request(
            serializer=self.serializer,
            instance=group,
        )
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
