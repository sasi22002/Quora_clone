from enum import Enum

class RoleEnum(Enum):
    superadmin=1
    user = 2


class GenderEnum(Enum):
    male = "Male"
    female = "Female"
    Not_to_say = None
    
    

class SocialTypeEnum(Enum):
    google = 1
    facebook = 2
    instagram = 3
    apple = 4
    twitter = 5
    


class ScreenEnum(Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    service ="service"
    badge = "badge"
    
    
class StaticEnum(Enum):
    forget_otp ="ForgetOtp"
    forget_password_otp ="Otp"
    forget_password_email ="Email"
    email_verify ="EmailVerify"
    forget_link="Link"
    cash_on_hand ="COH"
    pending = "Pending"
    in_progress = "In-Progress"
    admin = "Admin"
    procurement = "Procurement"
    new = "New"
    requested = "Requested"
    timeformatT = "%Y-%m-%dT%H:%M:%S"
    accepted = "Accepted"
    completed = "Completed"
    rejected = "Rejected"
    bussiness = 2
    questions = 1
    job = "Job"
    week="week"
    month="month"
    year="year"    
    country = 1
    state =2
    city =3
    empty = ""
    IND ="IND"
    USA="USA"
    empty_array = []
    lead = "lead"
    decline = "decline"
    notify_list = "notifylist"
    type ="type"
    Quora = "Quora"



class FileTypeEnum(Enum):
    excel = 1
    csv = 2
    tsv = 3
    pdf = 4
    

class EmailTypeEnum(Enum):
    rand_password = 1
    welcome_mail = 2
    forget_password_user = 3
    forget_password_admin = 4
    resend_otp = 5
    admin_delete_user = 6
    

class EmailEnum(Enum):
    reset_password_content = "Use this link to reset your password"    
    forgetmail_subject ="forget password"
    sample_pasword = "Use this password to login"
    email_verify = "Use this OTP to verify your email"
    email_verify_subject = "Email verification"
    account_info = "Account Credentials"
    welcome_mail = "Welcome Mail"
    account_deletes = "Account Deleted"
    docs_verified = "Documents Verification"
    
    
class EmailBodyEnum(Enum):
    send_password = "Use this password to login your account "
    weclome_mail = "You are now signed in as student Your user name is {0}"
    forget_password_otp = "Use this OTP {0} to reset your password"
    forget_password_link ="Use this link to reset your password   {0}/{1}/{2}"
    account_deleted_Admin = "Your account is currently deleted by Admin"
    document_verified = "Your documents are verified by admin"
    documents_declined = "Your documents are declined by admin"
    

class EmailFileEnum(Enum):
    delete_admin_user = "admin_delete_user.html"
    welcome_otp = "welcome_otp.html"
    cat_verification = "certificate_verify.html"
    static_file = "staticfile.html"
    

class JobStatusEnum(Enum):
    all = 1
    open_job = 1
    priced = 2
    scheduled = 3
    accepted = 4
    completed = 5
    deleted = 6
    canceled = 7

class JobFilterEnum(Enum):
    all_jobs = 1
    job_accepting_prices = 2
    accepted_prices = 3
    jobs_in_scheduling = 4
    job_appointment = 5
    job_waits_review = 9
    completed_jobs = 6
    cancel_jobs = 7
    prices_waits_acceptance = 2  #sp side filters
    prices_in_scheduling = 4  #sp side filters
    prices_appointment = 5  #sp side filters
    in_person_price_completed = 8  #sp side filters
    
    

class JobTypeEnum(Enum):
   price_it = 1
   in_person = 2



class ServiceProviderEnum(Enum):
   individual = "individual"
   business = "Business"



class QuoteEnum(Enum):
   price_it="price_it"
   in_person_quote="in_person_quote"

class NotificationTypeEnum(Enum):
    new_job = 1 #sp
    new_question = 2 # for cust side
    new_price = 3 #cust
    price_accepted = 4 #sp side
    job_scheduled = 5 #
    job_scheduled_sp = 6 # cust
    completed = 7 #sp 
    sp_completed = 8 #cust
    review = 9
    review_sp = 10 #cust
    reminder = 11
    reminder_sp = 12 #cust
    news_offer = 13
    question_reply =14 #sp
    cancel_job = 15 #sp
    scheduled_Accepted = 16 #sp
    scheduled_Accepted_sp = 17 #cust
    
    
class NotificationSubjectEnum(Enum):
    new_lead = "New Lead - Quora"
    price_accepted = "Price Accepted - Quora"
    new_question = "New Question Posted - Quora"
    question_reply = "Question Answered - Quora"
    new_price = "New Price - Quora"
    scheduling = "Jobs Time Scheduling - Quora"
    completed = "Job Completed - Quora"
    sp_completed = "Job Complete Request - Quora"
    wait_to_review = "Job Review - Quora"
    reminders = "Reminders - Quora"
    news_offer = "News & Offers - Quora"
    
    

class SPDocumentsStatus(Enum):
    new = "new"
    approve = "approved"
    reject ="rejected"
    
   

class SuperEnum(Enum):    
    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}
    
    
    @classmethod
    def values(cls):
        """Returns a list of all the enum values."""
        return list(cls._value2member_map_.keys())
    
    
    @classmethod
    def values_array(cls):
        """Returns a list of all the enum values."""
        return list(e.value for e in cls)
    

#keys to remove in export files
Remove_keys = [
    "updated_at"
]

class PaymentStatus(Enum):
   unpaid="unpaid"
   paid="paid"
   cancelled="cancelled"


class AvailabilityEnum(Enum):
    immediate = 1
    this_Week = 2
    next_week = 3
    upon_req = 4
    
class QuoteEnum(Enum):
    price_it = 1
    in_person = 2

class StatesEnum(Enum):
    CA = "CA"

class CountryEnum(Enum):
    USA = "USA"

class SortingEnum(Enum):
    name_asc="name_ascending"
    name_desc="name_descending"
    email_asc="email_ascending"
    email_desc="email_descending"
    id_desc="id_descending"
    id_asc="id_ascending"
    block="block"
    unblock="unblock"