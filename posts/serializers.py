from rest_framework import serializers
from .models import Post, Comment, Like

# Serializer for comments
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user', 'post', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)  
    like_count = serializers.SerializerMethodField()  

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "updated_at", "comments", "like_count"]

    def get_like_count(self, obj):
        return obj.likes.count()
