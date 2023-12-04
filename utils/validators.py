import logging,copy
from utils.enum import RoleEnum


def signup_validator(data,screen):
    try:
        if data['role'] == RoleEnum.service_provider.value:
            if screen == 1:            
                json_keys=['username' ,'role',"email","phone_number","password","confirm_password"]
            if screen == 2:
                json_keys = ["user_id","services"]   
            if screen == 3:
                json_keys = ["user_id","role","liability","trade_license"]
        
        if data['role'] == RoleEnum.customer.value:
            if screen == 1:            
                json_keys=['username' ,'role',"email","phone_number","password","confirm_password","address"]
            
       
        for val in json_keys:
            if  val not in dict.keys(data):
                return False
        return True
    
    except Exception as e:
        logging.info(e)
        return False
    

def socialsignup_validator(data,screen):
    try:
        if data['role'] == RoleEnum.service_provider.value:
            if screen == 1:            
                json_keys=['username' ,'role',"email","phone_number","social_id","social_type"]
            if screen == 2:
                json_keys = ["user_id","services"]   
            if screen == 3:
                json_keys = ["user_id","role","liability","trade_license"]
        
        if data['role'] == RoleEnum.customer.value:
            if screen == 1:            
                json_keys=['username' ,'role',"email","phone_number","address","social_id","social_type"]
            
        for val in json_keys:
            if  val not in dict.keys(data):
                return False
        return True
    
    except Exception as e:
        logging.info(e)
        return False

def null_key_validator(request):
    try:
        data=copy.deepcopy(request.data)
        
        if 'profile_picture' in data:
            del data['profile_picture']
        for val in data:
            if len(str(request.data[val])) == 0 or request.data[val] == None:
                return False
        return True
    except Exception as e:
        logging.info(e)
        return False



def create_adminstaff_validator(request):
    try:
        data=request.data
        json_keys=['username' ,'email','role']
        for val in json_keys:
            if  val not in dict.keys(data):
                return False
        return True
    except Exception as e:
        logging.info(e)
        return False


def service_category_create_validator(data):
    try:
        json_keys =['category_name','icon','description']
        json_vals =['category_name','icon','description']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_vals:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}
    

def service_category_update_validator(data):
    try:
        json_keys =['category_code','category_name','icon','description']
        json_vals =['category_code','category_name','icon','description']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_vals:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}
    

    

def createjob_validator(data):
    try:
       
        json_keys=["images","title","description","measurements","geo_location","services","job_deadline"]
            
        for val in json_keys:
            if  val not in dict.keys(data):
                return False
        return True
    
    except Exception as e:
        logging.info(e)
        return False


def admin_docs_accept(data):
    try:
        json_keys =['service_provider','status']
        json_vals =['status']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_vals:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
        
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}
    

def location_update(data):
    try:
        json_keys =['id','city_name']
        json_vals =['city_name']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_vals:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
        
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}


def question_update(data):
    try:
        json_keys =['id','question']
        json_vals =['question']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_vals:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
        
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}
    

def admin_creation(data):
    try:
        json_keys =['username','email','phone_number']

        for key in json_keys:
            if  key not in dict.keys(data):
                return {'data':key +" key is missing",'status':False}
        
        for val in json_keys:
            if len(data[val]) == 0:
                return {'data':val+" value is required",'status':False}
        
        return {'status':True}
    except Exception as e:
        return {'data':str(e)+" Internal Error",'status':False}