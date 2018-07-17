from django.db import models

# Create your models here.
class TvShow(models.Model):
    name = models.CharField(max_length=120)
    rating = models.FloatField(default=0)
    def __str__(self):
        return self.name

class Season(models.Model):
    show = models.ForeignKey(TvShow,related_name='season')
    name = models.CharField(max_length=120)
    rating= models.FloatField(default=0)
    def  __str__(self):
        return self.show.name + '|' + self.name

class Episode(models.Model):
    season = models.ForeignKey(Season,related_name='episode')
    position = models.CharField(max_length=120)
    name = models.CharField(max_length=120,blank=True)
    rating = models.FloatField(default=0)
    def __str__(self):
        return self.season.show.name+'|'+ self.season.name + '|'+ self.position + '|'+ self.name
