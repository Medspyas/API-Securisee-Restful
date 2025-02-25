from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from softdesk.permissions import IsIssueAuthorOrContributor
from projects.models import Contributor
from .models import Issue
from .serializers import IssueSerializer


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssueAuthorOrContributor]

    def get_queryset(self):
        # Récupère toutes les issues d'un projet auquel l'utilisateur est contributeur.
        return Issue.objects.select_related("author", "project").filter(
            project__contributors__user=self.request.user
        )

    def perform_create(self, serializer):
        # Permet à un contributeur de créer une issue relative à un projet.
        project = serializer.validated_data["project"]

        if not Contributor.objects.filter(
            user=self.request.user, project=project
        ).exists():
            raise PermissionDenied(
                "Vous devez être contributeur du projet pour crée une issue"
            )

        assignee = serializer.validated_data.get("assignee", None)
        if (
            assignee
            and not Contributor.objects.filter(user=assignee, project=project).exists()
        ):
            raise PermissionDenied("L'assigné doit être contributeur du projet")
        serializer.save(author=self.request.user)
