import uuid
from django.db import models
from django.conf import settings
from issues.models import Issue

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=2000, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue , on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
