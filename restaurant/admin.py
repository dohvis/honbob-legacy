from django.contrib import admin
from restaurant.models import Restaurant, Review, Links, Images

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Links)
admin.site.register(Images)

# Register your models here.
