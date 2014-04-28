from django.db import models

class Passwords(models.Model):
    userName = models.CharField(max_length=64)
    userPasswd = models.CharField(max_length=64)
    comments = models.CharField(max_length=128)
