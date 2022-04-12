from rest_framework import serializers
from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_comment_count(self, obj):
        return obj.parent_post.count()


class CommentSerializer(serializers.ModelSerializer):
    is_parent = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'is_edited',
                  'is_parent', 'created_at', 'children', ]

    def get_is_parent(self, obj):
        return obj.is_parent

    def get_children(self, obj):
        serializer = CommentSerializer(obj.children, many=True, context={
                                       'request': self.context.get('request')})
        return serializer.data
