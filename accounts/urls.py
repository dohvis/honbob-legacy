from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from accounts import views
urlpatterns = [
    url(r'', include('allauth.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
]
