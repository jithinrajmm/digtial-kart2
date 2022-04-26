from twilio.rest import Client 
from django.conf import settings
    
    
account_sid = settings.ACCOUNT_SID 
auth_token = settings.AUTH_TOKEN  
client = Client(account_sid, auth_token) 
    

def send_sms(user_code,phone_number):
    message = client.messages.create(  
                                messaging_service_sid= settings.MESSAGING_SERVICE_SID, 
                                body=f'{user_code}',      
                                to=f'{phone_number}') 