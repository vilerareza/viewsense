from django.contrib.auth.hashers import UNUSABLE_PASSWORD_SUFFIX_LENGTH
from django.db import models

# Create your models here.

class Account(models.Model):
    userName = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.userName
