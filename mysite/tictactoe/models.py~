from django.db import models

class History(models.Model):
    owner = models.IntegerField()
    result = models.CharField(max_length=16)
    created = models.DateTimeField()

    def __unicode__(self):

        if self.result.lower() == 'user_lost' :
            result_str = 'lost'
        elif self.result.lower() == 'user_won' :
            result_str = 'won'
        else:
            result_str = 'draw'
        
        return '%s  %s' % (result_str, self.created)



       
