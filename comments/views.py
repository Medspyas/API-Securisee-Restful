from .models import Comment, Contributor
from projects.models import Project
from .serializers import CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied



