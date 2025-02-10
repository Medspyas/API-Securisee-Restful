from .models import Issue, Contributor
from .serializers import IssueSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(project__contributors__user=self.request.user)
    
    def perform_create(self, serializer):

        project = serializer.validated_data['project']

        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionDenied("Vous devez être contributeur du projet pour crée une issue")
        
        assignee = serializer.validated_data.get('assignee', None)
        if assignee and not Contributor.objects.filter(user=self.request.user, project=project).exists():
            raise PermissionDenied("L'assigné doit être contributeur du projet")
        serializer.save(author=self.request.user)
