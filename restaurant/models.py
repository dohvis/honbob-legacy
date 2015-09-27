from django.db import models
from accounts.models import User

class Images(models.Model):
    link = models.ForeignKey('Links', related_name='images')    
    img = models.ImageField()

class Links(models.Model):
    Restaurant = models.ForeignKey('Restaurant', related_name='links')
    url = models.CharField(max_length=256)

class Restaurant(models.Model):
    title = models.CharField(max_length=64)
    address = models.CharField(max_length=128, null=True)
    x = models.FloatField()
    y = models.FloatField()
    
class Review(models.Model):
    Restaurant = models.ForeignKey(Restaurant, related_name='reviews')
    user = models.ForeignKey(User, related_name='recently_visit')
    rate = models.IntegerField()
    comment = models.CharField(max_length=500)

