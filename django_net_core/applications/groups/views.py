from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from applications.frontend.services import pagination
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
    serializer = serializers.CreationGroupSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request: Request):
        serializer = create.create_new_group_from_api_request(
            request=request,
            serializer=self.serializer
        )
        return Response({'success': 'new group was created.'})


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


class AlterGroupAPIView(APIView):
    serializer = serializers.GroupSerializer

    def post(self, request: Request):
        serializer = create.create_new_group_from_api_request(
            request=request,
            serializer=self.serializer
        )
        return Response({'new group': serializer.data})

    def put(self, request: Request, group_slug: str):
        group = read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        serializer = update.update_group_from_api_request(
            request=request,
            serializer=self.serializer,
            instance=group
        )
        return Response({'updated group': serializer.data})

    def delete(self, request: Request, group_slug: str):
        group = read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        serializer = delete.delete_group_from_api_request(
            serializer=self.serializer,
            instance=group
        )
        return Response({'deleted group': serializer.data})

