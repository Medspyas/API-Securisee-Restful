from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from projects.models import Contributor
from softdesk.permissions import IsCommentAuthorOrContributor

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrContributor]

    def get_queryset(self):
        # Récupération tous les commentaires lié à une issue qui appartient un projet
        # où l'utilisateur est contributeur.
        return Comment.objects.select_related("author", "issue").filter(
            issue__project__contributors__user=self.request.user
        )

    def perform_create(self, serializer):
        # Permet de créer un commentaire lié à une issue
        # d'un utilisateur qui est contributeur.
        issue = serializer.validated_data["issue"]

        if not Contributor.objects.filter(
            user=self.request.user, project=issue.project
        ).exists():
            raise PermissionDenied(
                "Vous devez être contributeur du projet pour crée un commentaire"
            )

        serializer.save(author=self.request.user)
