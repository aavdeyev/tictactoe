from django.db import models

class History(models.Model):
    owner = models.IntegerField()
    result = models.CharField(max_length=16)
    created = models.DateTimeField()

    # This will print a game record in game history    
    def __unicode__(self):
        if self.result.lower() == 'user_lost' :
            result_str = 'lost'
        elif self.result.lower() == 'user_won' :
            result_str = 'won'
        else:
            result_str = 'draw'
        
        return '%s  %s' % (result_str, self.created)

class GameState(models.Model):
    owner = models.IntegerField()
    sqrs = models.CharField(max_length=9)
    step_num = models.IntegerField()
    branch = models.CharField(max_length=16)
    status = models.CharField(max_length=16)   



       
