from django.db import models

class History(models.Model):
    owner = models.IntegerField()
    result = models.CharField(max_length=8)
    created = models.DateTimeField()

    def __unicode__(self):

        if self.result.lower() == 'userlost' :
            result_str = 'lost'
        elif self.result.lower() == 'userwin' :
            result_str = 'won'
        else:
            result_str = 'draw'
        
        return '%s  %s' % (result_str, self.created)



       
