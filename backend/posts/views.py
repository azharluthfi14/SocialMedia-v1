from django.shortcuts import get_object_or_404
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from rest_framework import status, viewsets, views, generics, exceptions, permissions
from core.pagination import CustomPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


class PostDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = CustomPagination


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save()


class CommentView(views.APIView):

    def get_object(self, pk):
        post = Post.objects.get(id=pk)
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        comment = Comment.objects.filter(
            post=post, parent=None).order_by('-created_at')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(comment, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, pk):
        data = request.data
        post = self.get_object(pk)

        if len(data.get('body')) < 1:
            raise exceptions.APIException('This field can not be blank.')

        new_comment = Comment(body=data.get('body'), post=post)
        new_comment.save()

        serializer = CommentSerializer(new_comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
