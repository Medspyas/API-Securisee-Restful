from rest_framework import serializers

from .models import Comment, Issue


class CommentSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ["id", "description", "issue", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time"]
