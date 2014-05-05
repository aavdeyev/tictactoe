from django.db import models

class History(models.Model):
    owner = models.IntegerField()
    result = models.CharField(max_length=8)
    created = models.DateTimeField()



       
