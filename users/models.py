from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError



class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.age is not None and self.age < 15:
            if self.can_data_be_shared:
                raise ValidationError("Les utilisateurs de moin de 15 ans ne peuvent pas partager leurs données")
        
