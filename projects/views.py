from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer, AddProjectSerializer

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_projects = Project.objects.filter(author=self.request.user) 
        

        contributed_projects = Project.objects.filter(contributors__user=self.request.user)

        return (user_projects | contributed_projects).distinct()
    
    def perform_create(self, serializer):
        
        project = serializer.save(author=self.request.user)

        Contributor.objects.create(user=self.request.user, project=project, role='author')
        print(f"Contributeur ajouté : {self.request.user} pour le projet {project.title}")




class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(project__author=self.request.user)
    
    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionDenied("Vous n'ête pas contributeur ou auteur de ce projet")
        serializer.save()

class AddContributorViewSet(ModelViewSet):
    serializer_class = AddProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.filter(project__author=self.request.user)
    
    def perform_create(self, serializer):

        project = serializer.validated_data['project']
        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut ajouter des contributeurs")
        user_to_add = serializer.validated_data['user']
        if Contributor.objects.filter(user=user_to_add, project=project).exists():
            raise PermissionDenied('Cet utilisateur est déja contributor')
        serializer.save()
       


