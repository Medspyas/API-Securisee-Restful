from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission

from comments.models import Comment
from issues.models import Issue
from projects.models import Contributor


class IsprojectAuthorOrContributor(BasePermission):
    # Définit les permissions d'accès à un projet
    def has_permission(self, request, view):
        # Donne accès à un utilisateur authentifié,
        # mais aussi contributeur du projet.
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(
                "Vous devez être authentifié pour accéder à cette ressource."
            )

        action = getattr(view, "action", None)

        if action == "retrieve":
            project_id = view.kwargs.get("pk")
            if not Contributor.objects.filter(
                user=request.user, project_id=project_id
            ).exists():
                raise PermissionDenied(
                    "Vous devez être contributeur pour accéder à ce projet"
                )

        if action == "list":
            if not Contributor.objects.filter(user=request.user).exists():
                raise PermissionDenied("Vous n'êtes contributeur d'aucun projet.")
        return True

    def has_object_permission(self, request, view, obj):
        # Permet à l'auteur de modifier et supprimer un projet.
        # Permet simplement à un contributeur de consulter un projet.
        if request.method in SAFE_METHODS:
            return True

        if obj.author != request.user:
            raise PermissionDenied(
                "Seul l'auteur peut modifier ou supprimer ce projet."
            )
        return True


class IsIssueAuthorOrContributor(BasePermission):
    # Définit les permissions d'accès à une issue
    def has_permission(self, request, view):
        # Donne accès à un utilisateur authentifié,
        # mais aussi contributeur du projet.
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(
                "Vous devez être authentifié pour accéder à cette ressource."
            )

        action = getattr(view, "action", None)

        if action == "retrieve":
            issue_id = view.kwargs.get("pk")
            issue = Issue.objects.filter(id=issue_id).first()
            if not issue:
                raise PermissionDenied("L'issue demandé n'existe pas.")
            if not Contributor.objects.filter(
                user=request.user, project=issue.project
            ).exists():
                raise PermissionDenied(
                    "Vous devez être contributeur pour voir cette issue"
                )

        if action == "list":
            if not Contributor.objects.filter(user=request.user).exists():
                raise PermissionDenied("Vous n'êtes contributeur d'aucun projet.")
        return True

    def has_object_permission(self, request, view, obj):
        # Permet à l'auteur de modifier et supprimer une issue.
        # Permet simplement à un contributeur de consulter une issue.
        if request.method in SAFE_METHODS:
            return True

        if obj.author != request.user:
            raise PermissionDenied(
                "Seul l'auteur peut modifier ou supprimer cette issue."
            )
        return True


class IsCommentAuthorOrContributor(BasePermission):
    # Définit les permissions d'accès à un commentaire
    def has_permission(self, request, view):
        # Donne accès à un utilisateur authentifié,
        # mais aussi contributeur du projet.
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(
                "Vous devez être authentifié pour accéder à cette ressource."
            )

        action = getattr(view, "action", None)

        if action == "retrieve":
            comment_id = view.kwargs.get("pk")
            comment = Comment.objects.filter(id=comment_id).first()
            if not comment:
                raise PermissionDenied("Le commentaire demandé n'existe pas.")
            if not Contributor.objects.filter(
                user=request.user, project=comment.issue.project
            ).exists():
                raise PermissionDenied(
                    "Vous devez être contributeur pour voir ce commentaire"
                )

        if action == "list":
            if not Contributor.objects.filter(user=request.user).exists():
                raise PermissionDenied("Vous n'êtes contributeur d'aucun projet.")
        return True

    def has_object_permission(self, request, view, obj):
        # Permet à l'auteur de modifier et supprimer un commentaire.
        # Permet simplement à un contributeur de consulter un commentaire.
        if request.method in SAFE_METHODS:
            return True

        if obj.author != request.user:
            raise PermissionDenied(
                "Seul l'auteur peut modifier ou supprimer ce commentaire."
            )
        return True
