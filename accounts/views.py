from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from accounts.models import User

def signup_handler(sender, user, request, **kwargs):
    extra_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
    user.gender = extra_data['gender']
    user.name = extra_data['name']
    user.email = extra_data['email']
    user.save()
    

def logout(request):
    print ("logout")
    logout(request)
    return HttpResponseRedirect('/')

def login_handler(sender, user, request, **kwargs):
    print(sender)
    print(user)
    print(request)

user_logged_in.connect(login_handler)
user_signed_up.connect(signup_handler)