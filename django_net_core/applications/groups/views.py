from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from django.http import Http404

from applications.groups import serializers
from applications.groups.services.crud import read, create, update, delete


class PublicGroupDetailAPIView(APIView):
    serializer = serializers.PublicGroupDetailSerializer

    def get(self, request: Request, group_slug: str):
        group = read.get_group_by_slug(group_slug)
        if not group:
            raise Http404

        serializer = self.serializer(group)
        return Response(serializer.data)


class PublicGroupListAPIView(APIView):
    serializer = serializers.PublicGroupListSerializer

    def get(self, request: Request):
        groups = read.get_all_groups()
        serializer = self.serializer(groups, many=True)
        return Response(serializer.data)


class PublicGroupPostDetailAPIView(APIView):
    serializer = serializers.PublicGroupPostDetailSerializer

    def get(self, request: Request, group_post_slug: str):
        post = read.fetch_group_post_with_comments(group_post_slug)
        if not post:
            raise Http404

        serializer = self.serializer(post)
        return Response(serializer.data)


class PublicGroupPostCommentListAPIView(APIView):
    serializer = serializers.PublicGroupPostCommentListSerializer

    def get(self, request: Request, group_post_slug: str):
        comments = read.get_all_comments_for_group_post_by_slug(group_post_slug)
        serializer = self.serializer(comments, many=True)
        return Response(serializer.data)


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

