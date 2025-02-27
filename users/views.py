from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Récupère les données, utilisateurs de l'auteur et de ceux auxquels 'can_data_be_shared' est vrai.
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(Q(id=user.id) | Q(can_data_be_shared=True))

    def create(self, request, *args, **kwargs):
        # Bloque la création d'utilisateur, d'un utilisateur authentifié.
        return Response(
            {"error": "Création d'utilisateur non autorisée"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def destroy(self, request, *args, **kwargs):
        # Permet à l'utilisateur de supprimer son compte.
        user = self.get_object()
        if user != request.user:
            return Response(
                {"error": "Vous ne pouvez supprimer que votre propre compte."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
         # Permet à l'utilisateur de modifier son compte.
        user = self.get_object()
        if user != request.user:
            return Response(
                {"error": "Vous ne pouvez modifier que votre propre compte."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)


class RegisterView(CreateAPIView):
    # C'est la section ou l'on créer son compte utilisateur.
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
