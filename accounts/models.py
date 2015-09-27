from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db.models import Q

class UserManager(BaseUserManager):

    def create_user(self, username, password, email=None, ages=None,name=None,school=None):
        if not username:
            raise ValueError('아이디를 입력해주세요.')
        user = self.model(username=username)
        user.set_password(password)
        user.email = email
        user.name = name
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        if not username:
            raise ValueError('아이디를 입력해주세요.')
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, help_text='아이디')
    is_staff = models.BooleanField(default=False, help_text='관리자 여부')
    is_active = models.BooleanField(default=True, help_text='계정 활성화 여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=64, null=True)
    gender = models.CharField(max_length=16, null=True)
    
    objects = UserManager()
    profile = None
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return ('<%s %s>' % (self.__class__.__name__, self.username))

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

