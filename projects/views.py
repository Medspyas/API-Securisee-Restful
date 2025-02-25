from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from softdesk.permissions import IsprojectAuthorOrContributor

from .models import Contributor, Project
from .serializers import ContributorSerializer, ProjectSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsprojectAuthorOrContributor]

    def get_queryset(self):
        # Permet à l'auteur et aux contributeurs d'accéder à un projet spécifique.
        user_projects = Project.objects.filter(author=self.request.user)

        contributed_projects = Project.objects.filter(
            contributors__user=self.request.user
        )

        return (user_projects | contributed_projects).distinct()

    def perform_create(self, serializer):

        project = serializer.save(author=self.request.user)

        Contributor.objects.create(
            user=self.request.user, project=project, role="author"
        )
        print(
            f"Contributeur ajouté : {self.request.user} pour le projet {project.title}"
        )


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Permet de récupérer les contributeurs d'un projet donné.
        return Contributor.objects.filter(
            Q(project__author=self.request.user)
            | Q(project__contributors__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        # Permet à l'auteur d'ajouter un contributeur un projet.
        project = serializer.validated_data["project"]
        user_to_add = serializer.validated_data["user"]

        if project.author != self.request.user:
            raise PermissionDenied(
                "Seul l'auteur du projet peut ajouter un contributeur."
            )

        if user_to_add == project.author:
            raise PermissionDenied(
                "L'auteur du projet est automatiquement contributeur et ne peut pas s'ajouter lui même"
            )

        if Contributor.objects.filter(user=user_to_add, project=project).exists():
            raise PermissionDenied("Cet utilisateur est déjà contribteur.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        # Permet à l'auteur de supprimer un contributeur.
        contributor = self.get_object()
        if contributor.project.author != request.user:
            return Response(
                {"detail": "Seul l'auteur du projet peut supprimer un contributeur."},
                status=403,
            )
        return super().destroy(request, *args, **kwargs)
