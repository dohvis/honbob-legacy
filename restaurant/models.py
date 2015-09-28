from django.db import models
from accounts.models import User
from location_field.models.plain import PlainLocationField

class Images(models.Model):
    link = models.ForeignKey('Links', related_name='images')    
    img = models.ImageField()

class Links(models.Model):
    Restaurant = models.ForeignKey('Restaurant', related_name='links')
    url = models.CharField(max_length=256)

class Restaurant(models.Model):
    title = models.CharField(max_length=64)
    address = models.CharField(max_length=128, null=True)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    location = PlainLocationField(zoom=16)

    def __str__(self):
        return "{}".format(self.title)

    def set_location(self):
        self.location = "{},{}".format(str(self.y),str(self.x))
        self.save()

class Review(models.Model):
    Restaurant = models.ForeignKey(Restaurant, related_name='reviews')
    user = models.ForeignKey(User, related_name='recently_visit')
    honbob_rate = models.IntegerField(default=5)
    taste_rate = models.IntegerField(default=5)
    etc_rate = models.IntegerField(default=5)
    comment = models.CharField(max_length=500)

