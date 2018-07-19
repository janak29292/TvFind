from django.db import models

# Create your models here.
class TvShow(models.Model):
    name = models.CharField(max_length=120,unique=True)
    number_of_seasons=models.CharField(max_length=5,blank=True,null=True)
    rating = models.CharField(max_length=5,blank=True,null=True)
    votes = models.CharField(max_length=64,blank=True,null=True)
    summary = models.TextField(blank=True,null=True)
    image=models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name

class Season(models.Model):
    show = models.ForeignKey(TvShow,related_name='season')
    name = models.CharField(max_length=120,blank=True,null=True)
    number_of_episodes=models.CharField(max_length=10,blank=True,null=True)
    rating= models.FloatField(default=None)
    def  __str__(self):
        return self.show.name + '|' + self.name

class Episode(models.Model):
    season = models.ForeignKey(Season,related_name='episode')
    position = models.CharField(max_length=120)
    name = models.CharField(max_length=120,blank=True,null=True)
    rating = models.FloatField(default=0)
    votes = models.CharField(max_length=12,blank=True,null=True)
    image=models.TextField(blank=True,null=True)
    summary=models.TextField(blank=True,null=True)
    date=models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.season.show.name+'|'+ self.season.name + '|'+ self.position + '|'+ self.name
