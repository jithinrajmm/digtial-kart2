from twilio.rest import Client 
    
    
account_sid = 'AC45a51315690af834c14f6f59ee6d8187' 
auth_token = '22b47aacc027e93cf52be6c222ec90a6' 
client = Client(account_sid, auth_token) 
    

def send_sms(user_code,phone_number):
    message = client.messages.create(  
                                messaging_service_sid='MG70764f27314c6a650e8dcc9052947390', 
                                body=f'{user_code}',      
                                to=f'{phone_number}') 