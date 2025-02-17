from rest_framework.viewsets import ModelViewSet
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    def create(self, request, *args, **kwargs):
        return Response({"error": "Création d'utilisateur non autorisée"}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            return Response({'error': "Vous ne pouvez supprimer que votre propre compte."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def get_serializer_context(self):
        return {"request": self.request}


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]