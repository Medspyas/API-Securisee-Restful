from .models import Comment
from projects.models import Contributor
from .serializers import CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from softdesk.permissions import IsCommentAuthorOrContributor 


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrContributor]

    def get_queryset(self):
        return Comment.objects.select_related('author', 'issue').filter(issue__project__contributors__user=self.request.user)
    
    def perform_create(self, serializer):

        issue = serializer.validated_data['issue']

        if not Contributor.objects.filter(user=self.request.user, project=issue.project).exists():
            raise PermissionDenied("Vous devez être contributeur du projet pour crée un commentaire")        
       
        serializer.save(author=self.request.user)


    
        