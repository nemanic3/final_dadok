from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
