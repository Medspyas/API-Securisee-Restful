import uuid

from django.conf import settings
from django.db import models

from issues.models import Issue


class Comment(models.Model):
    # Représente le modèle d'un commentaire
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=2000, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.author.username} - {self.issue.title}"
