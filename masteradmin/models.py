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
    profile_picture = models.TextField(null=True,blank=True)
    social_id = models.TextField(null=True)
    social_type = models.IntegerField(null=True)
    is_block = models.BooleanField(default= False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)   
    last_login = models.DateTimeField(blank=True,null=True)
    block_reason = models.CharField(max_length=100,null=True)
    

    class Meta:
        db_table = 'auth_master'

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
   


class UserRole(models.Model):
    """
    Args:
        models : Model for mapping user with respective roles
    """
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='user_role',null = True,blank=True)
    user=models.ForeignKey(User,related_name='userrole_user',null=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(default= True)
    
    class Meta:
        db_table = 'user_roles'
        
        

class UserActivityLog(models.Model):
    """
    Args:
        models: Model for save the User activity details with API payload data
    """
    user=models.ForeignKey(User,related_name='user_activity',null=True,on_delete=models.CASCADE)
    activity_details = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)
              
    class Meta:
        db_table = 'activity_log'


class UserSession(models.Model):
    """
    Args:
        models : Model for save the User Sessions with Access/Refresh tokens
    """
    access_token = models.TextField()
    refresh_token = models.TextField(null=True)
    auth=models.ForeignKey(User,related_name='auth_session',null=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    sessiontext = models.TextField(max_length=220)
    loggedin_as = models.IntegerField(null=True)


    class Meta:
        db_table = 'user_session'
        
        

class UserFollow(models.Model):
    """
    Args:
        models : Model for map the User Followers & Following details
    """
    follower=models.ForeignKey(User,related_name='follower_user',null=False,on_delete=models.CASCADE)
    followed_by=models.ForeignKey(User,related_name='followed_user',null=False,on_delete=models.CASCADE)    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)


    class Meta:
        db_table = 'quora_follow_user'
                       

class PostMaster(models.Model):
    """
    Args:
        models : Model for User posts/questions list
    """
    auth_master=models.ForeignKey(User,related_name='post_user',null=False,on_delete=models.CASCADE)
    content = models.TextField(null=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)

    class Meta:
        db_table = 'quora_post_master'
        
        
        

class PostComments(models.Model):
    """
    Args:
        models : Model for post answers&comment replies User
    """
    auth_master=models.ForeignKey(User,related_name='post_comment_user',null=False,on_delete=models.CASCADE)
    comment_reply=models.ForeignKey('self',related_name='post_comment_reply',null=True,on_delete=models.CASCADE)
    content = models.TextField(null=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)

    class Meta:
        db_table = 'quora_post_comments'
        
        

class PostLikes(models.Model):
    """
    Args:
        models :Model for count of user liked posts 
    """
    auth_master=models.ForeignKey(User,related_name='post_like_user',null=False,on_delete=models.CASCADE)
    post_master = models.ForeignKey(PostMaster,related_name='post_like',null=False,on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)

    class Meta:
        db_table = 'quora_post_likes'
        

class PostCommentLikes(models.Model):
    """
    Args:
        models : Model for user postanswer likes & postcomment replies likes
    """
    auth_master=models.ForeignKey(User,related_name='comment_like_user',null=False,on_delete=models.CASCADE)
    post_master = models.ForeignKey(PostComments,related_name='post_comment_like',null=False,on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null = True)
    updated_at = models.DateTimeField(auto_now=True,null = True)

    class Meta:
        db_table = 'quora_postcomment_likes'
        