from rest_framework import serializers
from .models import Issue


class IssueSerializer(serializers.ModelSerializer):
    
    created_time = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)   
    class Meta:
        model = Issue
        fields = ['id','title', 'description', 'priority', 'tag', 'status', 'assignee', 'project', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']