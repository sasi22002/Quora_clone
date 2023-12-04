from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,BaseUserManager
)

from utils.enum import GenderEnum
from django.contrib.auth.models import BaseUserManager



class Role(models.Model):
    """
    User roles
    1 - ADMIN
    2 - USER

    Args:
        models (_type_):user roles
    """
    role_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default= True)
    class Meta:
        db_table = 'role_master'
        

# User related tables
class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField(max_length=126, unique=True,null = False)
    username = models.CharField(max_length =60)
    password = models.CharField(max_length=256,null = True,blank = True)
    phone_number=models.CharField(max_length=128,null=True,unique=True)
    address = models.CharField(max_length=256,null = True)
    date_of_birth = models.CharField(max_length=16,blank=True,null=True)
    gender = models.CharField(max_length=8,default=GenderEnum.Not_to_say.value,blank=True,null=True)
    geo_location = models.TextField(null=True,blank=True)
    profile_picture = models.TextField(null=True,blank=True)
    social_id = models.TextField(null=True)
    social_type = models.IntegerField(null=True)
    is_block = models.BooleanField(default= False)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)   
    last_login = models.DateTimeField(blank=True,null=True)
    block_reason = models.CharField(max_length=100,null=True)
    is_deleted= models.BooleanField(default=False)
    latitude = models.TextField(null=True,blank=True)
    longtitude = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'auth_master'

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
   


class UserRole(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='user_role',null = True,blank=True)
    user=models.ForeignKey(User,related_name='userrole_user',null=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(default= True)
    
    class Meta:
        db_table = 'user_roles'
        
        

class UserActivityLog(models.Model):
    user=models.ForeignKey(User,related_name='user_activity',null=True,on_delete=models.CASCADE)
    activity_details = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)
              
    class Meta:
        db_table = 'activity_log'


class UserSession(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField(null=True)
    auth=models.ForeignKey(User,related_name='auth_session',null=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    sessiontext = models.TextField(max_length=220)
    loggedin_as = models.IntegerField(null=True)


    class Meta:
        db_table = 'user_session'
        