from django.db import models
from django.conf import settings
from projects.models import Project, Contributor
from django.core.exceptions import ValidationError

class Issue(models.Model):

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    BUG = 'bug'
    FEATURE = 'feature'
    TASK = 'task'

    TO_DO = 'To Do'
    IN_PROGRESS = 'In Progress'
    FINISHED = 'Finished'

    PRIORITY_CHOICES = [(LOW, 'Low'), (MEDIUM, 'Medium'), (HIGH, 'High')]
    TAG_CHOICES = [(BUG, 'Bug'),(FEATURE, 'Feature'),(TASK, 'Task')]
    STATUS_CHOICES = [(TO_DO, 'To Do'), (IN_PROGRESS, 'In Progress'), (FINISHED, 'Finished')]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues_created')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,on_delete=models.CASCADE, related_name='issues_assigned')
    priority = models.CharField(max_length=7, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=8, choices=TAG_CHOICES)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=TO_DO)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.assignee:
            if not Contributor.objects.filter(user=self.assignee, project=self.project).exists():
                raise ValidationError("L' utilisateur assigné doit être contributeur du projet")
    


