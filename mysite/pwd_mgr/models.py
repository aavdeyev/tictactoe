from django.db import models

from django.contrib.auth.models import User

class pwdMgrModel(models.Model):
    description = models.CharField(max_length=64)
    userName = models.CharField(max_length=64)
    passwd = models.CharField(max_length=64)
    comments = models.CharField(max_length=128)
    created = models.DateTimeField()
    owner = models.IntegerField()
