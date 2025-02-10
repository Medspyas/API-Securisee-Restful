from django.db import models
from django.conf import settings



class Project(models.Model):
    BACKEND = 'back-end'
    FRONTEND = 'front-end'
    IOS = 'iOS'
    ANDROID = 'Android'

    CHOICES_TYPE =[
        (BACKEND, 'Back-End'),
        (FRONTEND, 'Front-End'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    ]


    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=10, choices=CHOICES_TYPE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contributor(models.Model):

    AUTHOR = "author"
    CONTRIBUTOR = "contributor"

    ROLES_TYPE = [(AUTHOR, 'Author'), (CONTRIBUTOR, 'Contributor')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributors")
    role = models.CharField(max_length=12, choices=ROLES_TYPE)
