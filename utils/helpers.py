from datetime import datetime,timedelta
import random,logging,math,json
from django.conf import settings
from django.core.mail import EmailMessage
from utils.enum import RoleEnum
from utils.enum import FileTypeEnum,StaticEnum
from masteradmin.models import User,UserRole,UserSession
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import json,logging,traceback,sys
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from io import BytesIO
from django.http import HttpResponse
import string, random
from quora.development import TIME_ZONE


# define a function to calculate the distance between two points in km





def generate_otp():
    # Define possible characters for OTP
    digits = "123456789"
    otp = ""
    # Loop to generate 6 random digits
    for i in range(4):
        otp += random.choice(digits)
    # Return the OTP
    return otp

def init_twilio():
    # SEND OTP TO CLIENT NUMBER
    try:
        # client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    
        # client.messages.create(to=phone_no,from_=settings.TWILIO_NUMBER,body=message)
        pass
        
    except Exception as e:
        raise Exception
   

def send_mail_woTemplate(subject,mail_body,to_mail,from_mail,**template_data):
    try:
        
        if template_data:
            content = template_data['content']
            template = template_data['template']
            html_content = render_to_string(template, content)
            email = EmailMultiAlternatives(subject=subject,body=mail_body,from_email=from_mail,to=[to_mail])
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            
        email = EmailMessage(
            subject=subject,body=mail_body,to=[to_mail],from_email=from_mail
        )
        email.send()
        return True
    except Exception as ex:
        raise ex
    
    

class Convertion:
    
    def getIST():
        return datetime.utcnow()+timedelta(hours=5,minutes=30)
    
    def getindian_time(data):        
        val=data + timedelta(hours=5,minutes=30)
        return val
    
    def convert_UTC(data):                
        if TIME_ZONE == StaticEnum.IND.value:
            val=data + timedelta(hours=5,minutes=30)
        else:
            val=data - timedelta(hours=7)
            
        return val
    
    def getGREECE():
        return datetime.utcnow()+timedelta(hours=2)
    
    def getgreece_time(data):        
        val=data + timedelta(hours=2)
        return val
    
    def getUTC():
        return datetime.utcnow()
            
    def convert_str_time(time):
        try:
            _sttime=time.strftime('%d %B %Y %I.%M %p')
            return _sttime
        except:
            logging.warning('error while converting')
            return time
        
        
    def convert_strptime_timezone(time):
        try:
            try:
                _sttime=datetime.strptime(time,'%Y-%m-%dT%H:%M:%S.%fz')
                return _sttime
            except:
                _sttime=datetime.strptime(time,'%Y-%m-%dT%H:%M:%Sz')
                return _sttime
            
        except:
            logging.warning('error while converting')
            return time
    
    
    def convert_strptime(time):
        try:
            try:
                _sttime=datetime.strptime(time,'%Y-%m-%d %H:%M:%S.%f')
                return _sttime
            except:
                _sttime=datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
                return _sttime
            
        except:
            logging.warning('error while converting')
            return time

    def convert_strptime_format(time,format):
        try:
            try:
                _sttime=datetime.strptime(time,format)
                return _sttime
            except:
                return _sttime
            
        except:
            logging.warning('error while converting')
            return time
    
    
        

        
def generate_randpassword(userid):
    try:
        import secrets
        from django.contrib.auth.hashers import make_password

        password_length = 6
        rand_passowrd = secrets.token_urlsafe(password_length)
        hash_passowrd = make_password(rand_passowrd)
        
        save_temppassword = User.objects.filter(id=userid).update(password=hash_passowrd)
        return rand_passowrd
        
    except Exception as e:
        raise Exception
        
        


def split_pagedatas(page,item):
    page = int(page)
    item = int(item)
    start = item *(page-1)
    end = item * page
    return [start,end]


def save_mail_history(user,email_data):
    try:
        mail_history = UserEmailHistory.objects.create(user_id=user,email_details=email_data) 
    except Exception as e:
        logging.info(f"{e}: save_mail_history")
        pass
    
    

    

class LogInfo:
    def __init__(self,error):
        logging.info(error)
        logging.error(traceback.format_exception(*sys.exc_info()))
        pass

    def return_response(error,message):
        logging.info(error)
        logging.error(traceback.format_exception(*sys.exc_info()))
        res = {'status':False,'message':message,'data':[]}
        return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
    
        
        

#create jwt token for a user
def auth_token(user,role):
    emp_id=User.objects.get(email=user.email).id
    access = AccessToken.for_user(user)
    refresh=RefreshToken.for_user(user)

    access['email']=user.email
    access['user_id']=emp_id
    access['role']=role
    refresh['email']=user.email
    refresh['user_id']=emp_id
    refresh['role']=role
    
    #sAVE LAST LOGIN TIME
    login_time = User.objects.filter(id=emp_id).update(last_login=datetime.now())
    
    save_user_sessionsdata(access,refresh,emp_id,role)
      
    return {"access_token": str(access),
    "refresh_token":str(refresh)}
    
    

def get_user_role(user):
    try:
        user_role = UserRole.objects.filter(user_id=user).last()
        return user_role.role.id
    except Exception as e:
        logging.info(f"{e}: get_user_role function")
        raise Exception
    

def login_details(user,role):
    try:
        user_details = {}
        get_jwt = auth_token(user,role)
        user_details['access_token'] = get_jwt['access_token']
        user_details['refresh_token'] = get_jwt['refresh_token']
        user_details['role'] = role
        user_details['email'] = user.email
        user_details['user_id'] = user.id
        user_details['user_name'] = user.username
        user_details['is_approved'] = user.is_approved
        user_details['is_rejected'] = user.is_rejected
        user_details['profile_pic'] = user.profile_picture
        if get_user_role(user)==RoleEnum.superadmin.value:
            user_details['is_superuser']=True
        else:
            user_details['is_superuser']=False        
        return user_details
        
    except Exception as e:
        logging.info(f"{e}: login details func")
        raise Exception
    
    

def generate_uniqueids(type):
    
    if str(type) == StaticEnum.job.value:        
        try:
            job_id = JobMaster.objects.filter(job_code__isnull=False).last()        
            count = 1
            while count < 10:
                job_id = job_id.job_code[4:]
                job_id = int(job_id) + count
                job_id = '{:01}'.format(job_id)
                job_id = "JOB_" + str(job_id)
                count += 1
                if JobMaster.objects.filter(job_code=job_id).count() == 0:
                    break
            return job_id
        
        except Exception as e:
            job_id = "JOB_" + "1"
            return job_id
        
        

def generate_sessionskeys():
    count =1
    while count < 10:
        length = 4
        possible_numbers = "1234567890"
        random_nummber_list = [random.choice(possible_numbers) for i in range(length)]
        random_num = "".join(random_nummber_list)
        char_length = 15
        possible_numbers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        random_nummber_list = [random.choice(possible_numbers) for i in range(char_length)]
        random_name = "".join(random_nummber_list)
        res = random_name +random_num
        check = UserSession.objects.filter(sessiontext=res).exists()
        if not check:
            break
        count += 1
    return res


def save_user_sessionsdata(access,refresh,empid,role):
    try:
       sessionkey = generate_sessionskeys()
       data = UserSession.objects.filter(auth_id=empid).exists()
       if data:
           update_ = UserSession.objects.filter(auth_id=empid).update(access_token=access,refresh_token=refresh,sessiontext=sessionkey,loggedin_as=role)
       else:
           create_ = UserSession.objects.create(auth_id=empid,access_token=access,refresh_token=refresh,sessiontext=sessionkey,loggedin_as=role)
    except Exception as e:
       logging.info(e,'sessions not saved')
       pass

def generate_password():
    letters= string.ascii_letters
    digits= string.digits
    alphabet= letters+ digits
    password=''
    for i in range(8):
        password+= ''.join(random.choice(alphabet))
    return password


def backup_user(id_):
    try:
        user = User.objects.filter(id=id_).last()
        user_obj = User.objects.filter(id=id_).prefetch_related('userrole_user')
        
        user_data = json.dumps(user_obj.values()[0], indent=4, sort_keys=True, default=str)
        
        [UserBackup(email=user.email,role_id=value,user_detail=user_data).save() for value in user_obj.values_list('userrole_user__role_id',flat=True)]
        
        
        return True
        
    except Exception as e:
        logging.info(e,'backup_user')
        pass