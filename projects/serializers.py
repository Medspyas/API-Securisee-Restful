from rest_framework import serializers
from .models import Project, Contributor
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_time = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)   

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['id', 'author', 'created_time']


class ContributorSerializer(serializers.ModelSerializer):    
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']
        read_only_fields = ['id', 'user']

   






    
