from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from restaurant import views
urlpatterns = [
    url(r'^list/(?P<min_x>\d*\.\d*)/(?P<min_y>\d*\.\d*)/(?P<max_x>\d*\.\d*)/(?P<max_y>\d*\.\d*)/$',
        views.serializer),
]
