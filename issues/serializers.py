from rest_framework import serializers

from users.models import User

from .models import Issue


class IssueSerializer(serializers.ModelSerializer):
    assignee = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        required=False,
        allow_null=True,
    )
    created_time = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "tag",
            "status",
            "assignee",
            "project",
            "author",
            "created_time",
        ]
        read_only_fields = ["author", "created_time"]
