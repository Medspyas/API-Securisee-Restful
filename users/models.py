from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Modèle de l'utilisateur avec ses champs spécifiques
    age = models.IntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.username}"
