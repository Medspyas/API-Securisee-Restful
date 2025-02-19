from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from softdesk.permissions import IsprojectAuthorOrContributor
from django.db.models import Q

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsprojectAuthorOrContributor]

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
        return Contributor.objects.filter(
            Q(project__author=self.request.user) | Q(project__contributors__user=self.request.user)).distinct()
    
    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        user_to_add = serializer.validated_data['user']

        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter un contributeur.")       
        
        
        if user_to_add == project.author:
            raise PermissionDenied("L'auteur du projet est automatiquement contributeur et ne peut pas s'ajouter lui même")
        
        if Contributor.objects.filter(user=user_to_add, project=project).exists():
            raise PermissionDenied("Cet utilisateur est déjà contribteur.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        contributor = self.get_object()
        if contributor.project.author != request.user:
            return Response({"detail": "Seul l'auteur du projet peut supprimer un contributeur."}, status=403)
        return super().destroy(request, *args, **kwargs)




