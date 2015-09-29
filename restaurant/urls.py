from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from restaurant import views
urlpatterns = [
    url(r'^list/$',
        views.serializer),
]
