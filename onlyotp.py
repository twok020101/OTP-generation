import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')

token = os.environ.get("token")
endpoint = os.environ.get("endpoint")

class ApiManagement:
    
    def __init__(self,number,otp) -> None:
        self.url = "https://"+endpoint+"/api/v1/"
        self.number=number
        self.otp=otp

    def sendOTP(self):
        url="https://"+endpoint+"/api/v1/sendTemplateMessage?whatsappNumber="+str("91"+str(self.number))
        headers = {
                "Content-Type": "text/json",
                "Authorization": token
            }
        payload = {
                "parameters": [
                    {
                        "name": "one_time_password",
                        "value": str(self.otp)
                    }
                ],
             
                "broadcast_name": "my",
                "template_name": "one_time_password_template"
            }
        response = requests.post(url, json=payload, headers=headers)
        return response

def main(number,otp):
    cust=ApiManagement(number,otp)
    return (cust.sendOTP()).text
