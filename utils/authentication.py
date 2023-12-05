from rest_framework import permissions,status
import logging
from utils.pagination import pagination_class,pagination_func
from utils.enum import EmailEnum, StaticEnum,EmailTypeEnum,JobStatusEnum,RoleEnum,ScreenEnum
from utils.validators import *
from django.utils import timezone
from django.contrib.auth import authenticate
from django.db import transaction
from utils.response_message import Message
from utils.decorator import *
from quora import settings
from rest_framework.views import APIView


class SignUp(APIView):
    permission_classes=[permissions.AllowAny]
    
    @transaction.atomic()
    def post(self,request):
        try:
            data=request.data
            screen = data['screen']

            #BASIC VALIDATIONS
            validate = signup_validator(data,screen)
            if not validate:
                res={'status':False,'message':Message.data_missing,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
            validate_null = null_key_validator(request)
            if not validate_null:
                res={'status':False,'message':Message.mandatory_keys,'data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
        
            try:
                old_user = User.objects.filter(email=data['email'],is_deleted=True).exists()
            except :
                old_user = User.objects.filter(email=data['user_id'],is_deleted=True).exists()
                
            if screen == ScreenEnum.one.value:
                check_phone = User.objects.filter(phone_number=data['phone_number'],is_deleted=False).exists()
                deleted_phone = User.objects.filter(phone_number=data['phone_number'],is_deleted=True).exclude(email=data['email']).exists()
                
                if check_phone or deleted_phone:
                    res={'status':False,'message':Message.phonenumber_exist,'data':[]}
                    return Response(res,status=status.HTTP_400_BAD_REQUEST) 
                
                if data['password'] != data['confirm_password']:
                    res={'status':False,'message':Message.password_mismatched,'data':[]}
                    return Response(res,status=status.HTTP_400_BAD_REQUEST)  
           
            if old_user:                
                user_data = recover_old_user(data)
            else:                              
                user_data = save_user(data)
            
                                                          
            res = {'status':True,'message':Message.registerd_success,'data':[user_data]}
            return Response(res,status=status.HTTP_200_OK)
          
        except Exception as e:
            transaction.set_rollback(True)
            logging.info(f"{e}: signup screen",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):
    """
    Login for All users
    
    """
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        try:
            email= request.data['email']          
            password = request.data['password']
            role = request.data['role']
            
            if email == None:
                res = {'status':False,'message':Message.enter_keys,'data':[],'screen_staus':None}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            if password == None:
                res = {'status':False,'message':Message.enter_password,'data':[],'screen_staus':None}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            email = User.objects.filter(email=email,userrole_user__role_id=role,is_deleted=False,social_id__isnull=True).prefetch_related('userrole_user').last() 
            if role==RoleEnum.superadmin.value:
                email = User.objects.filter(email=request.data['email'],is_deleted=False).last() 
                
            if not email:
                res = {'status':False,'message':Message.register_mail,'data':[],'screen_staus':None}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
            if role == RoleEnum.superadmin.value:
                email = User.objects.filter(email=email).last()
                user = authenticate(request, email=email.email, password=password)
            if role == RoleEnum.admin.value:
                user = authenticate(request, email=email.email, password=password)
            if role == RoleEnum.service_provider.value:
                user = authenticate(request, email=email.email, password=password)
            if role == RoleEnum.customer.value:           
                user = authenticate(request, email=email.email, password=password)
                                            
            if user is None:
                res = {'status':False,'message':Message.invalid_password,'data':[],'screen_staus':None}
                return Response(res,status = status.HTTP_400_BAD_REQUEST) 
            
            if user.is_block:
                res = {'status':False,'message':Message.login_block,'data':[],'screen_staus':None}
                return Response(res,status = status.HTTP_400_BAD_REQUEST)
            
            user_data = login_details(user,role)
            res = {'status':True,'message':Message.login_success,'data':[user_data],'screen_staus':check_screen_status(user.id)}
            return Response(res,status=status.HTTP_200_OK)
                          
        except Exception as e:
            logging.info(f"{e}: Login",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

        
    def post(self,request):
        try:
            user = request.user.id

            UserSession.objects.filter(auth_id=user).update(is_active=False)
            #remove device token
            UserDeviceTokenMaster.objects.filter(auth_master_id=user).delete()
            
            res = {'status':True,'message':Message.logout_success,'data':[]}
            return Response(res,status=status.HTTP_200_OK)
            
        except Exception as e:
            logging.info(f"{e}: Logout",exc_info=True)
            res = {'status':False,'message':Message.server_error,'data':[]}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        